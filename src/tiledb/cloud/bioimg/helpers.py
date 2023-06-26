import math
import os
from typing import Any, Iterator, Mapping, Sequence, Tuple

import tiledb


def get_uris(
    source: Sequence[str], output_dir: str, config: Mapping[str, Any], output_ext: str
):
    """Match input uri/s with output destinations

    :param source: A sequence of paths or path to input
    :param output_dir: A path to the output directory
    """
    vfs = tiledb.VFS(config=config)

    def create_output_path(input_file, output_dir) -> str:
        return os.path.join(output_dir, os.path.basename(input_file) + f".{output_ext}")

    def iter_paths(sequence) -> Iterator[Tuple]:
        for uri in sequence:
            yield uri, create_output_path(uri, output_dir)

    if len(source) == 1 and vfs.is_dir(source[0]):
        # Check if the dir is actually a tiledb group for exportation
        with tiledb.scope_ctx(ctx_or_config=config):
            if tiledb.object_type(source[0]) != "group":
                # Folder like input
                return tuple(iter_paths(vfs.ls(source[0])))
            else:
                # This is the exportation scenario
                return ((source[0], create_output_path(source[0], output_dir)),)
    elif isinstance(source, Sequence):
        # List of input uris - single file is one element list
        return tuple(iter_paths(source))


def serialize_filter(filter):
    if isinstance(filter, tiledb.Filter):
        filter_dict = filter._attrs_()
        filter_dict["_name"] = type(filter).__name__
        return filter_dict
    else:
        raise TypeError


def batch(iterable, chunks):
    # Iterator for providing batches of chunks
    length = len(iterable)
    for ndx in range(0, length, chunks):
        yield iterable[ndx : min(ndx + chunks, length)]


def scale_calc(source, num_batches):
    """Calculate scaling settings for batch_size and max_workers

    :param source: The source iterable containing files to be ingested/exported
    :param num_batches: The number of batches given by the API
    :return: Tuple batch_size, max_workers
    """
    # If num_batches is default create number of images nodes
    # constraint node max_workers to 20 fully heuristic
    if num_batches is None:
        num_batches = len(source)
        batch_size = 1
        max_workers = 20
    else:
        batch_size = math.ceil(len(source) / num_batches)
        max_workers = None

    return batch_size, max_workers
