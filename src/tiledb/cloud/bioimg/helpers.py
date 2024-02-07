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


def validate_io_paths(source: Sequence[str], output: Sequence[str]) -> None:
    if len(source) == 0 or len(output) == 0:
        raise ValueError("Source/Output list must not be empty.")

    if len(source) == 1 and len(output) == 1:
        if is_folder(source[0]) and not is_folder(output[0]):
            raise ValueError("Invalid combination of source and output paths.")
        else:
            return
    else:
        if len(source) == len(output):
            if all(not is_folder(s) for s in source) and all(
                not is_folder(o) for o in output
            ):
                return
            else:
                raise ValueError("Invalid combination of source and output paths.")
        else:
            raise ValueError("Invalid combination of source and output paths.")
