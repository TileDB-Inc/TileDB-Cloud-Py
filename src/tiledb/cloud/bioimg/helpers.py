import logging
import math
import os
from typing import Any, Iterator, Mapping, Sequence, Tuple

import tiledb
from tiledb.cloud.utilities import get_logger


def get_logger_wrapper(
    verbose: bool = False,
) -> logging.Logger:
    """
    Get a logger instance and log version information.

    :param verbose: verbose logging, defaults to False
    :return: logger instance
    """

    level = logging.DEBUG if verbose else logging.INFO
    logger = get_logger(level)

    logger.debug(
        "tiledb.cloud=%s, tiledb=%s, libtiledb=%s",
        tiledb.cloud.version.version,
        tiledb.version(),
        tiledb.libtiledb.version(),
    )

    return logger


_SUPPORTED_EXTENSIONS = (".tiff", ".tif", ".svs", ".tdb")


def get_uris(
    source: Sequence[str], output_dir: str, config: Mapping[str, Any], output_ext: str
):
    """Match input uri/s with output destinations

    :param source: A sequence of paths or path to input
    :param output_dir: A path to the output directory
    """
    vfs = tiledb.VFS(config=config)

    def create_output_path(input_file, output_dir) -> str:
        filename = os.path.splitext(os.path.basename(input_file))[0]
        return os.path.join(output_dir, filename + f".{output_ext}")

    def iter_paths(sequence) -> Iterator[Tuple]:
        for uri in sequence:
            if uri.endswith(_SUPPORTED_EXTENSIONS):
                yield uri, create_output_path(uri, output_dir)

    if len(source) == 1:
        if source[0].startswith("tiledb://"):
            # Support tiledb uri single image
            return ((source[0], create_output_path(source[0], output_dir)),)
        elif vfs.is_dir(source[0]):
            # Check if the dir is actually a tiledb group for exportation on VFS
            with tiledb.scope_ctx(ctx_or_config=config):
                if tiledb.object_type(source[0]) != "group":
                    # Folder like input
                    contents = vfs.ls(source[0])
                    if len(contents) != 0:
                        return tuple(iter_paths(contents))
                    else:
                        raise ValueError(
                            "Input bucket should contain images for ingestion"
                        )
                else:
                    # This is the exportation scenario for single tdb image
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


def scale_calc(samples, num_batches):
    """Calculate scaling settings for batch_size and max_workers

    :param source: The source iterable containing files to be ingested/exported
    :param num_batches: The number of batches given by the API
    :return: Tuple batch_size, max_workers
    """
    # If num_batches is default create number of images nodes
    # constraint node max_workers to 20 fully heuristic
    batch_size = 1 if num_batches is None else math.ceil(len(samples) / num_batches)
    max_workers = 20 if num_batches is None else None
    return batch_size, max_workers
