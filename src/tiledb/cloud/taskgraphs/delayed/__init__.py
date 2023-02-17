"""``delayed``, a simplified interface for task graphs.

This can be imported either as a namespace, or with ``import *``::

    from ... import delayed
    d_func = delayed.udf(some_func)(...)
    d_sql = delayed.sql(...)

or::

    from ....delayed import *
    d_func = Delayed(some_func)(...)
    d_sql = DelayedSQL(...)
"""

from tiledb.cloud.taskgraphs.delayed import _udf

udf = _udf.DelayedFunction.create
Delayed = udf

__all__ = ("Delayed",)
