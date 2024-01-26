import logging

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


def validate_io_paths(source, output):
    if isinstance(source, str):
        # Handle only lists
        if source.endswith("/"):
            # Source is folder
            if not isinstance(output, str):
                # Output is list of possible 1 or multiple records
                if not (len(output) == 1 and output[0].endswith("/")):
                    raise ValueError(
                        "For directory input the output should be also a \
                        directory with a trailing '/'"
                    )
            else:
                # Output is one record
                if not output.endswith("/"):
                    raise ValueError(
                        "For directory input the output should \
                        be also a directory with a trailing '/'"
                    )
        else:
            # Source is a file
            if not isinstance(output, str):
                # If 1 record list and folder allow
                if len(output) != 1:
                    raise ValueError(
                        "Single file input cannot correspond \
                        to multiple files output"
                    )

    elif not isinstance(source, str):
        if isinstance(output, str):
            if len(source) == 1:
                if source.endswith("/"):
                    if not output.endswith("/"):
                        raise ValueError(
                            "For dir sources the output should \
                            point to a dir with a trailing '/'"
                        )
            else:
                if not output.endswith("/"):
                    raise ValueError(
                        "For multiple inputs the output should \
                        correspond to a dir with a trailing '/'"
                    )
        else:
            if len(source) != len(output):
                if not all(not s.endswith("/") for s in source):
                    raise ValueError(
                        "For multiple inputs in source list \
                        the inputs cannot contain a dir"
                    )
                else:
                    if len(output) == 1:
                        if not output[0].endswith("/"):
                            raise ValueError(
                                "For multiple files in source list \
                                the output should be a unique folder"
                            )
                    else:
                        raise NotImplementedError(
                            "Multiple inputs containing dirs \
                            with multiple outputs is not supported"
                        )
            else:
                if len(source) != 1:
                    for z, o in zip(source, output):
                        if z.endswith("/") or o.endswith("/"):
                            raise NotImplementedError(
                                "Sequence of multiple inputs \
                                can only contain files and not directories"
                            )
                else:
                    if source[0].endswith("/") and not output[0].endswith("/"):
                        raise ValueError(
                            "For dir sources the output should point \
                            to a dir with a trailing '/'"
                        )
    return source, output
