"""Trampoline function to execute functions from installed libraries.

This exists to make it easy for code not written in Python to access and execute
installed Python functions in UDFs without having to register a specific UDF
for each function that the non-Python code might want to access. It is intended
for internal consumption by the TileDB Cloud UI.
"""

import importlib


def run_python_function(__name, *args, **kwargs):
    """Executes the named function with the given args and kwargs.

    This executes the function named with `the syntax used by the setuptools
    ``entry_points`` system`__: ``module:object[.attribute]*``. For instance,
    the function ``join`` in the ``os.path`` module is specified as
    ``os.path:join``.

    Arguments and kwargs are passed directly to the function.

    .. __: https://setuptools.pypa.io/en/latest/userguide/entry_point.html#entry-points-syntax
    """  # noqa: E501

    def _find_object(name: str):
        mod_name, sep, member_name = name.partition(":")
        result = importlib.import_module(mod_name)
        while sep:
            first, sep, member_name = member_name.partition(".")
            result = getattr(result, first)
        return result

    func = _find_object(__name)
    return func(*args, **kwargs)  # type: ignore
