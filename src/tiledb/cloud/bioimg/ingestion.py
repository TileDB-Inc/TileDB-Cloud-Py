from typing import Sequence, Union, Tuple, Mapping, Any, Optional
import tiledb
import math
import os
from tiledb.cloud.utils import logger
from functools import partial

def ingest(source: Union[Sequence[str], str],
           output: str, 
           access_key_id: str, 
           secret_access_key: str, 
           *,
           taskgraph_name: Optional[str] = None,
           num_batches: Optional[int] = 1,
           threads: Optional[int] = 8,
           resources: Optional[Mapping[str, Any]] = None,
           **kwargs):
    
    """The function ingests microscopy images into TileDB arrays

    :param source: uri / iterable of uris of input files e.g 
    :param output: output dir for the ingested tiledb arrays
    :param access_key_id: AWS_ACCESS_KEY_ID
    :param secret_access_key: AWS_SECRET_ACCESS_KEY
    :param taskgraph_name: Optional name for taskgraph, defaults to None
    :param num_batches: Number of graph nodes to spawn performs it sequentially if default, defaults to 1
    :param threads: Number of threads for node side multiprocessing, defaults to 8
    :param resources: configuration for node specs e.g. {"cpu": "8", "memory": "4Gi"} , defaults to None
    """

    if isinstance(source, str):
        # Handle only lists
        source = [source]

    # Calculate number batches - default fair split
    
    def batch(iterable, chunks):
        length = len(iterable)
        for ndx in range(0, length, chunks):
            yield iterable[ndx:min(ndx + chunks, length)]
   
    batch_size = math.ceil(len(source) / num_batches)

    # Get the list of all BioImg samples input/out
    samples = get_uris(source, output)

    # Build the task graph
    logger.info(f'Building graph')
    graph = tiledb.cloud.dag.DAG(name="batch-ingest-bioimg" if taskgraph_name is None else taskgraph_name,  
                                 mode=tiledb.cloud.dag.Mode.BATCH)

    for i, work in enumerate(batch(samples, batch_size)):
        logger.info(f"Adding batch {i}")
        graph.submit(
            ingest_tiff_udf,
            work,
            access_key_id,
            secret_access_key,
            threads,
            name=f"BioImg Ingest Batch - {i}/{num_batches}",
            mode=tiledb.cloud.dag.Mode.BATCH,
            resources={"cpu": "8", "memory": "4Gi"} if resources is None else resources,
            image_name="3.9-imaging-dev"
        )

    res = graph.compute()
    graph.wait()
    print(res)


def ingest_tiff_udf(io_uris: Sequence[Tuple], 
                     key: str, 
                     secret: str,
                     workers: int,
                     ):
    """Internal udf that ingests server side batch of bioimaging files into tiledb arrays using tiledb-bioimg API

    :param io_uris: Pairs of tiff input - output tdb uris
    :param key: AWS_ACCESS_KEY_ID
    :param secret: AWS_SECRET_ACCESS_KEY
    :param workers: Number of threads that will spawn for parallelizing ingestion
    """

    from tiledb.bioimg.converters.ome_tiff import OMETiffConverter

    conf = tiledb.cloud.Config()
    conf["vfs.s3.aws_access_key_id"] = key
    conf["vfs.s3.aws_secret_access_key"] = secret
    ctx = tiledb.cloud.Ctx(conf)
    vfs = tiledb.VFS(ctx)

    with tiledb.scope_ctx(ctx_or_config=ctx):
        for input, output in io_uris:
            with vfs.open(input) as src:
                OMETiffConverter.to_tiledb(src, output, max_workers=workers, chunked=True)

def get_uris(source: Union[Sequence[str], str], 
              output_dir: str):
    """Match input uri/s with output destinations

    :param source: A sequence of paths or path to input 
    :param output_dir: A path to the output directory
    """

    def create_output_path(input_file, output_dir):
        return os.path.join(output_dir, os.path.basename(input_file) + ".tdb")
    
    if isinstance(source, str):
        # Single file input
        return source, create_output_path(source, output_dir)
    else:
        # List of input uris
        result = []
        output_uris = []
        for uri in source:
            result.append(uri)
            output_uris.append( create_output_path(uri, output_dir))
        return tuple(zip(result, output_uris))
    