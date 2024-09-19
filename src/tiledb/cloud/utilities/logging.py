"""Logging."""

import logging
import sys
from typing import Optional

import tiledb
import tiledb.cloud
import tiledb.libtiledb


def get_logger(level: int = logging.INFO, name: str = __name__) -> logging.Logger:
    """
    Get a logger with a custom formatter and set the logging level.

    :param level: logging level, defaults to logging.INFO
    :param name: logger name, defaults to __name__
    :return: Logger object
    """

    sh = logging.StreamHandler(stream=sys.stdout)
    formatter = logging.Formatter(
        "[%(asctime)s] [%(module)s] [%(funcName)s] [%(levelname)s] %(message)s"
    )
    sh.setFormatter(formatter)

    logger = logging.getLogger(name)
    # Only add one handler, in case get_logger is called multiple times
    if not logger.handlers:
        logger.addHandler(sh)
        logger.setLevel(level)

    return logger


def get_logger_wrapper(
    verbose: bool = False,
    level: Optional[int] = None,
) -> logging.Logger:
    """
    Get a logger instance and log version information.

    Nominal use-case is a simple two-level approach: verbose or not.

    Using ``level`` provides access to the ``logging`` package's levels.

    :param verbose: verbose logging, defaults to False
    :param level: if provided, supersedes ``verbose`` and applies the
      requested level.
    :return: logger instance
    """

    if level is None:
        level = logging.DEBUG if verbose else logging.INFO
    logger = get_logger(level)

    logger.debug(
        "Configured logger: tiledb.cloud=%s, tiledb=%s, libtiledb=%s",
        tiledb.cloud.__version__,
        tiledb.version(),
        tiledb.libtiledb.version(),
    )

    return logger
