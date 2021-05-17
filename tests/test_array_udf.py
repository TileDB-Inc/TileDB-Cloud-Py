import tiledb, tiledb.cloud
import sys, os, platform, unittest, tempfile
import numpy, numpy as np

from tiledb import Dim, Domain, Attr, ArraySchema
from tiledb.cloud import client
from tiledb.cloud import array
from tiledb.cloud import tasks
from tiledb.cloud import tiledb_cloud_error


class ArrayUDFTests(unittest.TestCase):
    def test_array_udf_datetime64(self):

        # TODO make a tiledb:// temp directory usable from the test harness
        uri = tempfile.mkdtemp()

        schema = ArraySchema(
          domain=Domain(*[
            Dim(name='dt', domain=(numpy.datetime64('1677-09-21T00:12:43.145224194'), numpy.datetime64('2262-04-11T23:47:16.854765807')), tile=10000, dtype='datetime64[ns]'),
          ]),
          attrs=[
            Attr(name='idx', dtype='int64'),
          ],
          cell_order='row-major',
          tile_order='row-major',
          capacity=100000,
          sparse=True,
          allows_duplicates=True,
        )
        tiledb.Array.create(uri, schema)

        dtstart = np.datetime64('2019-01-01')
        dtstart_int = dtstart.astype("M8[ns]").astype(np.int64)
        dtend = np.datetime64('2019-01-02')
        coords = np.arange(dtstart_int, dtstart_int + 10)

        with tiledb.open(uri, "w") as A:
            A[coords] = np.random.randint(0, 100, 10)

        breakpoint()

        with tiledb.open(uri) as A:
            # TODO check that all of these are equivalent
            A.apply(lambda x: x, [(dtstart, dtend)])
            A.apply(lambda x: x, [(dtstart, None)])
            A.apply(lambda x: x, [(None, None)])
            A.apply(lambda x: x, [(None, dtend)])
