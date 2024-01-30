import logging
from typing import Sequence

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


def serialize_filter(filter):
    if isinstance(filter, tiledb.Filter):
        filter_dict = filter._attrs_()
        filter_dict["_name"] = type(filter).__name__
        return filter_dict
    else:
        raise TypeError


def is_folder(path: str) -> bool:
    return path.endswith("/")


def validate_io_paths(source: Sequence[str], output: Sequence[str]):
    if not isinstance(source, list) or not isinstance(output, list):
        raise ValueError("Both source and output must be lists.")

    if len(source) == 0:
        raise ValueError("Source list must not be empty.")

    # Case 1: If source is a list of files
    if all(not is_folder(path) for path in source):
        # Destination is a folder
        if len(output) == 1 and is_folder(output[0]):
            return True
        # Destination has the same number of paths with source - rename at destination
        elif len(output) == len(source) and all(not is_folder(path) for path in output):
            return True

    # Case 2: If source is a list with length one
    elif len(source) == 1:
        if is_folder(source[0]):
            if len(output) == 1 and is_folder(output[0]):
                return True
        else:
            if len(output) == 1 and (is_folder(output[0]) or not is_folder(output[0])):
                return True

    raise ValueError("Invalid combination of source and output paths.")
