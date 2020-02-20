import inspect
import logging

logger = logging.getLogger("tiledb.cloud")


def getsourcelines(func):
    if func is not None and not callable(func):
        raise TypeError("func argument to `apply` must be callable!")

    # try to include the original source code
    try:
        # get source lines to serialize with UDF
        # (functions defined in files may not always be available)
        source_lines = inspect.getsourcelines(func)[0]
        return "".join(source_lines)
    except Exception as exc:
        logger.warning(
            "Failed to serialize function source text, proceeding with bytecode only: %s".format(
                exec
            )
        )

    return None
