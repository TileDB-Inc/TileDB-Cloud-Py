from typing import Callable

import pandas as pd
import pyarrow as pa
from typing_extensions import Concatenate, ParamSpec


def _df_transform_result(
    table: pa.Table,
    fn: Callable[[pd.DataFrame], pd.DataFrame],
) -> pa.Table:
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


_PS = ParamSpec("_PS")


def df_transform(
    fn: Callable[Concatenate[pd.DataFrame, _PS], pd.DataFrame]
) -> Callable[_PS, Callable[[pa.Table], pa.Table]]:
    """
    A function decorator that streamlines creation of a user-defined function that
    transforms a pandas dataframe. The decorated function can be passed directly
    to the `transform_result` parameter of the `tiledb.cloud.vcf.query` function.

    :param fn: user-defined function that takes a pandas dataframe as input and
        returns a pandas dataframe
    :return: a function that can be passed to the `transform_result` parameter of
        the `tiledb.cloud.vcf.query` function
    """

    def wrapper(
        *args: _PS.args, **kwargs: _PS.kwargs
    ) -> Callable[[pa.Table], pa.Table]:
        return lambda tbl: _df_transform_result(
            tbl,
            lambda df: fn(df, *args, **kwargs),
        )

    return wrapper
