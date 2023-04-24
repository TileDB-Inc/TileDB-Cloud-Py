"""Utilities for dealing with functions for serialization and registration."""

import inspect
import types
from typing import Callable, Optional, TypeVar, Union

_T = TypeVar("_T")
Funcable = Union[str, Callable[..., _T]]
"""Either a Python function or the name of a registered UDF."""
_builtin_function = type(len)
"""The type of functions implemented in C."""


def to_register_by_value(__fn: types.FunctionType) -> types.FunctionType:
    """Converts the given function into one that can be registered "by value".

    When a function is serialized by reference, the result is roughly equivalent
    to ``import module.where.it.lives; module.where.it.lives.the_fn(...)``.
    When it is serialized by value, the function's (compiled) code is serialized
    and used at the receiving end to execute directly.

    This by itself does not *guarantee* that a function pickled by value will be
    usable. The same restrictions apply as to existing functions. For instance,
    if the function refers to globals from a module not importable at the
    destination, it still won't work.
    """

    if not isinstance(__fn, types.FunctionType):
        raise TypeError(
            "Only regular functions (not methods or built-in functions)"
            " may be converted to register-by-value."
        )

    # The value of a __module__ is (part of) how cloudpickle decides whether
    # to serialize a function by reference or by value.  It assumes that if
    # a function has a __module__ and is available in that module, it should
    # be importable on the receiving end (with some exceptions).  If it has no
    # __module__, or the __module__ is "__main__", it will always serialize
    # by value.
    #
    # This is a fancy way of copying everything but a function's __module__
    # to a new function object, without mutating the original.
    # Alas, copy.copy and copy.deepcopy both return the original instance
    # when used to copy a function object.

    new_fn = types.FunctionType(
        __fn.__code__, globals=__fn.__globals__, closure=__fn.__closure__
    )
    # We don't want the two objects to share the same __dict__ reference.
    new_fn.__dict__.update(__fn.__dict__)
    new_fn.__module__ = "<pickled data>"  # fictitious.
    # Special function attributes:
    # https://docs.python.org/3.11/reference/datamodel.html#index-33
    for attr in (
        "__doc__",
        "__name__",
        "__qualname__",
        # __module__: already set
        "__defaults__",
        # __code__: already set
        # __globals__: read-only, already set
        # __dict__: copied entry-by-entry above
        # __closure__: read-only, already set
        "__annotations__",
        "__kwdefaults__",
    ):
        try:
            setattr(new_fn, attr, getattr(__fn, attr))
        except AttributeError:
            pass  # It's fine if it's missing or unset on the original.
    return new_fn


def check_funcable(**kwargs) -> None:
    """Checks whether the given parameter can be treated as a function.

    For a function like::

        def process(some_func: Funcable, more, params):
            utils.check_funcable(some_func=some_func)
            # ...

    If it's a Funcable, then execution continues as normal. If not, then
    it raises an informative exception.
    """
    name, func = kwargs.popitem()
    assert not kwargs, "Too many args passed to _check_funcable"
    if callable(func) or type(func) == str:
        return
    raise TypeError(
        f"{name} argument must be a callable or the registered name of a UDF, "
        f"not {type(func)}"
    )


def full_name(f: Funcable) -> str:
    """Generates a "full name" to the given function for human reference."""
    if isinstance(f, str):
        return f"registered UDF {f!r}"
    try:
        if f.__module__:
            return f"{f.__module__}.{f.__qualname__}"
        return f.__qualname__
    except AttributeError:
        return str(f)


def getsourcelines(func: Callable) -> Optional[str]:
    """Attempt to extract the source code of ``func``, but accept failure."""
    if isinstance(func, _builtin_function):
        # Built-in functions have no accessible source code.
        return None
    try:
        # Attempt to find and serialize the original source...
        return "".join(inspect.getsourcelines(func)[0])
    except Exception:
        pass
    return None


def signature_of(src: Callable) -> Callable[[_T], _T]:
    """Decorator that applies the signature of ``func`` to the wrapped function.

    This allows autocomplete tools, like in Jupyter notebooks or IPython,
    to use function signature information from the source function when
    providing help for users about the destination function.

    In this example, users will be able to see prompts for ``b`` or ``c``
    when they press ``Tab`` while writing a call to  ``iter_a``:

    >>> def a(b, c):
    ...   return f'Hello, {b}! I am {c}.'
    >>> @signature_of(a)
    ... def iter_a(*args, **kwargs):
    ...   yield a(*args, **kwargs)
    """

    def copy_to(dst):
        dst.__signature__ = inspect.signature(src)
        return dst

    return copy_to
