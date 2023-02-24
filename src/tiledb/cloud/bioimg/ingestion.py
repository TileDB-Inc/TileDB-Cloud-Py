import math
import os
from functools import partial
from typing import Any, Mapping, Optional, Sequence, Tuple, Union

import tiledb
from tiledb.cloud.utils import logger


def ingest(source: Union[Sequence[str], str],
           output: str, 
           config: Mapping[str, Any], 
           *,
           taskgraph_name: Optional[str] = None,
           num_batches: Optional[int] = None,
           threads: Optional[int] = 8,
           resources: Optional[Mapping[str, Any]] = None,
           **kwargs):
    
    """The function ingests microscopy images into TileDB arrays

    :param source: uri / iterable of uris of input files
    :param output: output dir for the ingested tiledb arrays
    :param config: dict configuration to pass on tiledb.VFS
    :param taskgraph_name: Optional name for taskgraph, defaults to None
    :param num_batches: Number of graph nodes to spawn performs it sequentially if default, defaults to 1
    :param threads: Number of threads for node side multiprocessing, defaults to 8
    :param resources: configuration for node specs e.g. {"cpu": "8", "memory": "4Gi"} , defaults to None
    """

    def ingest_tiff_udf(io_uris: Sequence[Tuple], 
                     config: Mapping[str, Any],
                     workers: int,
                     ):
        
        """Internal udf that ingests server side batch of bioimaging files into tiledb arrays using tiledb-bioimg API

        :param io_uris: Pairs of tiff input - output tdb uris
        :param config: dict configuration to pass on tiledb.VFS
        :param workers: Number of threads that will spawn for parallelizing ingestion
        """

        from tiledb.bioimg.converters.ome_tiff import OMETiffConverter

        conf = tiledb.Config(params=config)
        vfs = tiledb.VFS(config=conf)

        with tiledb.scope_ctx(ctx_or_config=conf):
            for input, output in io_uris:
                with vfs.open(input) as src:
                    OMETiffConverter.to_tiledb(src, output, max_workers=workers, chunked=True)

    if isinstance(source, str):
        # Handle only lists
        source = [source]

    # Calculate number batches - default fair split
    
    def batch(iterable, chunks):
        length = len(iterable)
        for ndx in range(0, length, chunks):
            yield iterable[ndx:min(ndx + chunks, length)]
   
    # If num_batches is default create number of images nodes
    # constraint node max_workers to 20 fully heuristic
    if num_batches is None:
        num_batches = len(source)
        batch_size = 1
        max_workers = 20
    else:
        batch_size = math.ceil(len(source) / num_batches)
        max_workers = None

    # Get the list of all BioImg samples input/out
    samples = get_uris(source, output)

    # Build the task graph
    logger.info(f'Building graph')
    graph = tiledb.cloud.dag.DAG(name="batch-ingest-bioimg" if taskgraph_name is None else taskgraph_name,  
                                 mode=tiledb.cloud.dag.Mode.BATCH,
                                 max_workers=max_workers)

    for i, work in enumerate(batch(samples, batch_size)):
        logger.info(f"Adding batch {i}")
        graph.submit(
            ingest_tiff_udf,
            work,
            config,
            threads,
            name=f"BioImg Ingest Batch - {i}/{num_batches}",
            mode=tiledb.cloud.dag.Mode.BATCH,
            resources={"cpu": "8", "memory": "4Gi"} if resources is None else resources,
            image_name="3.9-imaging-dev"
        )

    graph.compute()
    graph.wait()


def get_uris(source: Sequence[str], 
              output_dir: str,
              config: Mapping[str, Any]):
    """Match input uri/s with output destinations

    :param source: A sequence of paths or path to input 
    :param output_dir: A path to the output directory
    """
    vfs = tiledb.VFS(config=config)

    def create_output_path(input_file, output_dir):
        return os.path.join(output_dir, os.path.basename(input_file) + ".tdb")
    

    def iter_paths(sequence):
        result = []
        output_uris = []
        for uri in sequence:
            result.append(uri)
            output_uris.append( create_output_path(uri, output_dir))
        return tuple(zip(result, output_uris))

    if vfs.is_dir(source):
        # Folder like input
        iter_paths(vfs.ls(source))
    elif isinstance(source, Sequence):
        # List of input uris - single file is one element list
        iter_paths(source)