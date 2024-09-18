import warnings
from typing import Sequence

import tiledb
import tiledb.cloud.utilities.logging


def serialize_filter(filter):
    if isinstance(filter, tiledb.Filter):
        filter_dict = filter._attrs_()
        filter_dict["_name"] = type(filter).__name__
        return filter_dict
    else:
        raise TypeError


def is_folder(path: str) -> bool:
    return path.endswith("/")


def validate_io_paths(
    source: Sequence[str], output: Sequence[str], *, for_registration: bool
) -> None:
    if len(source) == 0 or len(output) == 0:
        raise ValueError("Source/Output list must not be empty.")

    if for_registration:
        if any(o.startswith("tiledb://") for o in output):
            raise ValueError(
                "Output sequence contains a tiledb URI"
                "and this cannot be re-registered."
            )
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


def get_logger_wrapper(*args, **kwargs):
    warnings.warn(
        "Bioimg's get_logger_wrapper() is deprecated, "
        "use tiledb.cloud.utilities.logging.get_logger_wrapper() instead.",
        DeprecationWarning,
        stacklevel=2,
    )
    return tiledb.cloud.utilities.logging.get_logger_wrapper(*args, **kwargs)
