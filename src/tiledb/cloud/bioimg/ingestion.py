from typing import Any, Dict, Mapping, Optional, Sequence, Tuple, Union, Iterator

import tiledb
from tiledb.cloud._common.utils import logger
from tiledb.cloud.bioimg.helpers import batch
from tiledb.cloud.bioimg.helpers import get_uris
from tiledb.cloud.bioimg.helpers import scale_calc
from tiledb.cloud.bioimg.helpers import serialize_filter
from .types import EMBEDDINGS

DEFAULT_RESOURCES = {"cpu": "8", "memory": "4Gi"}
DEFAULT_IMG_NAME = "3.9-imaging-dev"
DEFAULT_DAG_NAME = "bioimg-ingestion"

# --------------------------------------------------------------------
# UDFs
# --------------------------------------------------------------------

def ingest_tiff_udf(
    io_uris: Sequence[Tuple],
    config: Mapping[str, Any],
    threads,
    embedding_model,
    embedding_level,
    embedding_grid,
    *args: Any,
    **kwargs,
):
    """Internal udf that ingests server side batch of bioimaging files
    into tiledb arrays using tiledb-bioimg API

    :param io_uris: Pairs of tiff input - output tdb uris
    :param config: dict configuration to pass on tiledb.VFS
    :param embedding_model: The model to be used for creating embedding. Supported values are of type class EMBEDDINGS
    :param embedding_level: The resolution level to be used for the embedding. This could be different from the ingestion level
    selected with parameter `level`
    :param embedding_grid: A tuple that represents the (num_of_rows, num_of_cols), in which the image will be splitted in patches
    for the embedding creation. According to this grid internally the image is being splitted to fit this requirement.
    """

    from tiledb import filter
    import numpy as np
    import os
    import tiledb.vector_search as vs
    from tiledb.bioimg.converters.ome_tiff import OMETiffConverter
    from tiledb.bioimg.openslide import TileDBOpenSlide
    from tiledb.cloud.bioimg.types import EMBEDDINGS
    
    compressor = kwargs.get("compressor", None)
    if compressor:
        compressor_args = dict(compressor)
        compressor_name = compressor_args.pop("_name")
        if compressor_name:
            compressor_args = {
                k: None if not v else v for k, v in compressor_args.items()
            }
            kwargs["compressor"] = vars(filter).get(compressor_name)(
                **compressor_args
            )
        else:
            raise ValueError

    conf = tiledb.Config(params=config)
    vfs = tiledb.VFS(config=conf)
    if embedding_model:
        # Calculate image embedding on image patches [arg=ResNet]
        def calculate_model(images_array: np.ndarray, model_id: EMBEDDINGS) -> np.ndarray:
            import tensorflow as tf
            from tensorflow.keras.applications.resnet_v2 import preprocess_input
            if model_id is EMBEDDINGS.RESNET:
                model = tf.keras.applications.ResNet50V2(include_top=False)
                maps = model.predict(preprocess_input(images_array))
                if np.prod(maps.shape) == maps.shape[-1] * len(images_array):
                    return np.squeeze(maps)
                else:
                    return maps.mean(axis=1).mean(axis=1)

        def get_embeddings_uris(output_file_uri: str) -> Tuple[str, str]:
            # The uri of the embeddings point inside the image group
            filename = os.path.basename(output_file_uri).split('.')[0]
            embeddings_flat_uri = os.path.join(output_file_uri, f'{filename}_embeddings_flat')
            embeddings_ivf_flat_uri = os.path.join(output_file_uri, f'{filename}_embeddings_ivf_flat')
            return embeddings_flat_uri, embeddings_ivf_flat_uri     

    with tiledb.scope_ctx(ctx_or_config=conf):
        for input, output in io_uris:
            with vfs.open(input) as src:
                OMETiffConverter.to_tiledb(src, output, **kwargs)
    
            if embedding_model:
                # Create the embeddings output paths
                embeddings_flat_uri, embeddings_ivf_flat_uri = get_embeddings_uris(output)

                # Split image [level=arg] in rectangular patches [arg] size
                def split_in_patches(image: np.ndarray, embedding_level: int, embedding_grid: Tuple[int,int]) -> Sequence[np.ndarray]:
                    level_shape_w, level_shape_h = image.level_dimensions[embedding_level]
                    # Calculate the region size based on the desired number of rows and columns
                    grid_row_num, grid_col_num = embedding_grid
                    region_height = level_shape_h // grid_row_num
                    region_width = level_shape_w // grid_col_num
                    # Loop through the image and extract each region
                    patches = []
                    for i in range(grid_row_num):
                        for j in range(grid_col_num):
                            location = (i, j)
                            patches.append(image.read_region(location, embedding_level, (region_height, region_width)))
                    return patches
                
                with TileDBOpenSlide(output) as image:
                    
                    # Filter out patches with [arg] % non-blank coverage
                    filtered = split_in_patches(image, embedding_level, embedding_grid)
            
                    patches_array = np.array([])
                    for patch in filtered:
                        patch_transformed = patch[np.newaxis]
                        if patches_array.any():
                            patches_array = np.concatenate((patches_array, patch_transformed), axis=0)
                        else:
                            patches_array = patch_transformed

                    # Create embedding of the image given its patches
                    embeddings = calculate_model(patches_array, embedding_model)
                    # Create flat index of the embedding for faster vector search
                    tmp_features_file = "/tmp/features"
                    with open(tmp_features_file, "wb") as f:
                        np.array(embeddings.shape, dtype="uint32").tofile(f)
                        np.array(embeddings).astype("float32").tofile(f)

                    vs.ingest(
                        index_type="FLAT",
                        index_uri=embeddings_flat_uri,
                        source_uri="features",
                        source_type="F32BIN",
                    )
                    vs.ingest(
                        index_type="IVF_FLAT",
                        index_uri=embeddings_ivf_flat_uri,
                        source_uri="features",
                        source_type="F32BIN",
                    )
                
                # Store embedding and flat index inside the image data model
                grp = tiledb.Group(output, "w")
                grp.add(embeddings_flat_uri)
                grp.add(embeddings_ivf_flat_uri)
                grp.meta["Embeddings Model"] = EMBEDDINGS.RESNET.name
                grp.meta["fmt_version"] = 3
                grp.close()        

                try:
                    os.remove(tmp_features_file)
                except OSError as e:
                    print(f"Error: {tmp_features_file} could not be deleted. {e}")


# --------------------------------------------------------------------
# User functions
# --------------------------------------------------------------------

def ingest(
    source: Union[Sequence[str], str],
    output: str,
    config: Mapping[str, Any],
    *args: Any,
    taskgraph_name: Optional[str] = None,
    num_batches: Optional[int] = None,
    threads: Optional[int] = 8,
    resources: Optional[Mapping[str, Any]] = None,
    compute: bool = True,
    namespace: Optional[str],
    embedding_model: Optional[EMBEDDINGS] = None,
    embedding_level: int = 0,
    embedding_grid: Tuple[int, int] = (4, 4),
    **kwargs,
) -> tiledb.cloud.dag.DAG:
    """The function ingests microscopy images into TileDB arrays

    :param source: uri / iterable of uris of input files
    :param output: output dir for the ingested tiledb arrays
    :param config: dict configuration to pass on tiledb.VFS
    :param taskgraph_name: Optional name for taskgraph, defaults to None
    :param num_batches: Number of graph nodes to spawn.
        Performs it sequentially if default, defaults to 1
    :param threads: Number of threads for node side multiprocessing, defaults to 8
    :param resources: configuration for node specs e.g. {"cpu": "8", "memory": "4Gi"},
        defaults to None
    :param compute: When True the DAG returned will be computed inside the function
    otherwise DAG will only be returned.
    :param namespace: The namespace where the DAG will run
    :param embedding_model: The model to be used for creating embedding. Supported values are of type class EMBEDDINGS
    :param embedding_level: The resolution level to be used for the embedding. This could be different from the ingestion level
    selected with parameter `level`
    :param embedding_grid: A tuple that represents the (num_of_rows, num_of_cols), in which the image will be splitted in patches
    for the embedding creation. According to this grid internally the image is being splitted to fit this requirement.
    """

    if isinstance(source, str):
        # Handle only lists
        source = [source]

    # Get the list of all BioImg samples input/out
    samples = get_uris(source, output, config, "tdb")
    batch_size, max_workers = scale_calc(samples, num_batches)

    # Build the task graph
    dag_name = taskgraph_name or DEFAULT_DAG_NAME
    task_prefix = f"{dag_name} - Task"

    logger.info("Building graph")
    graph = tiledb.cloud.dag.DAG(
        name=dag_name,
        mode=tiledb.cloud.dag.Mode.BATCH,
        max_workers=max_workers,
        namespace=namespace,
    )

    # serialize udf arguments
    compressor = kwargs.pop("compressor", None)
    compressor_serial = serialize_filter(compressor) if compressor else None

    for i, work in enumerate(batch(samples, batch_size)):
        logger.info(f"Adding batch {i}")
        graph.submit(
            ingest_tiff_udf,
            work,
            config,
            threads,
            embedding_model,
            embedding_level,
            embedding_grid,
            *args,
            name=f"{task_prefix} - {i}/{num_batches}",
            mode=tiledb.cloud.dag.Mode.BATCH,
            resources=DEFAULT_RESOURCES if resources is None else resources,
            image_name=DEFAULT_IMG_NAME,
            compressor=compressor_serial,
            **kwargs,
        )

    if compute:
        graph.compute()
    return graph

def ingest_udf(*args: Any, **kwargs: Any) -> Dict[str, str]:
    """Ingestor wrapper function that can be used as a UDF."""
    grf = ingest(*args, **kwargs)
    return {"status": "started", "graph_id": str(grf.server_graph_uuid)}
