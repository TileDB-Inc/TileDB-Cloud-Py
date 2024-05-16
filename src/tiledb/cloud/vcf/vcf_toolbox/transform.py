import functools
from typing import Callable, TypeVar

import pyarrow as pa


def _df_transform_result(table: pa.Table, fn) -> pa.Table:
    """
    Transform the pyarrow table using a user-defined function that operates on
    a pandas dataframe.

    :param table: pyarrow table
    :param fn: user-defined function to transform the pandas dataframe
    :return: pyarrow table
    """

    # Return if the table is empty
    if table.num_rows == 0:
        return table

    # Store the original schema
    original_schema = table.schema

    # Convert arrow table to pandas
    df = table.to_pandas()

    # Run user-defined transform function
    df = fn(df)

    # Convert the DataFrame back to a table
    result = pa.Table.from_pandas(df)

    # Cast the columns to the original data types because pandas may change the
    # column type for partitions where the results are all null.
    for field in original_schema:
        if field.name in result.column_names:
            result = result.set_column(
                result.column_names.index(field.name),
                field.name,
                pa.array(result.column(field.name).to_pandas(), type=field.type),
            )

    return result


_CT = TypeVar("_CT", bound=Callable)


def df_transform(fn: _CT) -> _CT:
    """
    A function decorator that allows users to create a user-defined function to
    transform a pandas dataframe. The decorated function can be passed directly
    to the `transform_result` parameter of the `tiledb.cloud.vcf.query` function.

    Parameters
    ----------
    fn
        The user-defined function that takes a pandas dataframe as input and
        returns a pandas dataframe.

    Returns
    -------
        A function than can be passed to the `transform_result` parameter of the
        `tiledb.cloud.vcf.query` function.
    """

    @functools.wraps(fn)
    def wrapper(*args, **kwargs):
        return functools.partial(
            _df_transform_result,
            fn=functools.partial(fn, *args, **kwargs),
        )

    return wrapper
