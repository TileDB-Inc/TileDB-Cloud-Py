from tiledb.cloud import array
from tiledb.cloud import utils
from tiledb.cloud._results import results


class CloudArray(object):
    @utils.signature_of(array.apply_async)
    def apply_async(self, *args, **kwargs) -> results.AsyncResult:
        """
        Apply a user-defined function to this array, asynchronously.

        Params are the same as :func:`array.apply_async`, but this instance
        provides the URI.
        """
        return array.apply_async(self.uri, *args, **kwargs)  # pylint: disable=E1101

    @utils.signature_of(array.apply)
    def apply(self, *args, **kwargs):
        """
        Apply a user-defined function to this array, synchronously.

        Params are the same as :func:`array.apply`, but this instance
        provides the URI.

        **Example**
        >>> import tiledb, tiledb.cloud, numpy
        >>> def median(df):
        ...   return numpy.median(df["a"])
        >>> # Open the array then run the UDF
        >>> with tiledb.SparseArray("tiledb://TileDB-Inc/quickstart_dense", ctx=tiledb.cloud.ctx()) as A:
        ...   A.apply(median, [(0,5), (0,5)], attrs=["a", "b", "c"])
        2.0
        """
        return array.apply(self.uri, *args, **kwargs)  # pylint: disable=E1101
