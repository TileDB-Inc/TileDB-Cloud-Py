import pyarrow as pa

from tiledb.cloud.sql._execution import exec
from tiledb.cloud.sql.db_api_exceptions import DataError
from tiledb.cloud.sql.db_api_exceptions import ProgrammingError


def _get_db_type(dtype):
    if pa.types.is_timestamp(dtype):
        return "DATETIME"
    elif pa.types.is_boolean(dtype):
        return "BOOLEAN"
    elif pa.types.is_string(dtype):
        return "STRING"
    elif pa.types.is_integer(dtype) or pa.types.is_floating(dtype):
        return "NUMBER"
    return "UNKNOWN"


class Cursor:
    def __init__(self):
        self._results = None
        self._row_index = 0
        self.arraysize = 1
        self._description_cache = None

    def executemany(self, query, seq_of_parameters):
        for params in seq_of_parameters:
            self.execute(query, params)

    def execute(self, query, params=()):
        try:
            self._description_cache = None
            self._results = exec(query=query, parameters=params, raw_results=True)
        except Exception as e:
            self._results = None
            raise DataError(f"Error executing query: {e}") from e

    def fetchmany(self, size=-1):
        if not self._results:
            raise DataError("Failed to fetch results")

        if size == -1:
            size = self.arraysize

        if size + self._row_index > len(self._results):
            # give all that is remaining
            size = len(self._results) - self._row_index

        if size == 0:
            # There are no more records
            return []

        rows = self._results[self._row_index : self._row_index + size]
        self._row_index += size
        return rows.to_pylist()

    def setinputsizes(self, sizes):
        return None

    def setoutputsize(self, size, column):
        return None

    @property
    def rowcount(self):
        return -1 if self._results is None else len(self._results)

    def fetchone(self):
        result = self.fetchmany(1)
        if len(result) == 0:
            return None
        return result[0]

    @property
    def description(self):
        if self._description_cache is not None:
            return self._description_cache

        if not self._results:
            return None

        description = [
            (field.name, _get_db_type(field.type), None, None, None, None, None)
            for field in self._results.schema
        ]
        self._description_cache = description
        return description

    def fetchall(self):
        if self._row_index > 0:
            return self.fetchmany(len(self._results) - self._row_index)
        if self._results is None:
            raise DataError("The query results are null")
        return self._results.to_pylist()

    def close(self):
        pass

    def reset(self):
        self._row_index = 0
        self.arraysize = 1

    def scroll(self, value, mode="relative"):
        if mode == "relative":
            new_index = self._row_index + value
        elif mode == "absolute":
            new_index = value
        else:
            raise ProgrammingError(
                f"Invalid mode {mode!r}. Please choose 'relative' or 'absolute'."
            )

        upper = len(self._results) - 1
        if not 0 <= new_index < upper:
            raise IndexError(f"Row index {new_index} is out of bounds (0 to {upper}).")

        self._row_index = new_index
