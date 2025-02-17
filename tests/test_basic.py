import ast
import subprocess
import sys
import unittest
import unittest.mock
import uuid

import numpy
import numpy as np
import packaging.version as pkgver
import pandas
import pyarrow
import pytest
import urllib3

import tiledb
import tiledb.cloud
from tiledb.cloud import array
from tiledb.cloud import client
from tiledb.cloud import groups
from tiledb.cloud import tasks
from tiledb.cloud import tiledb_cloud_error
from tiledb.cloud._common import json_safe
from tiledb.cloud._common import testonly


class BasicTests(unittest.TestCase):
    @unittest.skipIf(
        pkgver.parse(pandas.__version__) < pkgver.parse("1.5"),
        "does not work if we have to patch Pandas",
    )
    def test_dont_import_pandas(self):
        # Get a list of all modules from a completely fresh interpreter.
        all_mods_str = subprocess.check_output(
            (sys.executable, "-c", "import sys, tiledb.cloud; print(list(sys.modules))")
        )
        all_mods = ast.literal_eval(all_mods_str.decode())
        assert "pandas" not in all_mods

    def test_info(self):
        self.assertIsNotNone(array.info("tiledb://TileDB-Inc/quickstart_sparse"))
        self.assertIsNotNone(groups.info("tiledb://TileDB-Inc/TileDB_101"))

    def test_list_shared_with(self):
        self.needsUnittestUser()
        with self.assertRaises(tiledb_cloud_error.TileDBCloudError):
            array.list_shared_with("tiledb://TileDB-Inc/quickstart_sparse"),

    def test_array_activity(self):
        self.needsUnittestUser()
        with self.assertRaises(tiledb_cloud_error.TileDBCloudError):
            array.array_activity("tiledb://TileDB-Inc/quickstart_sparse")

    def test_tasks(self):
        self.assertIsNotNone(tasks.fetch_tasks(page=1, per_page=100))

    def test_list_arrays(self):
        self.assertIsNotNone(client.list_arrays().arrays)

    def test_list_shared_arrays(self):
        self.needsUnittestUser()
        self.assertIsNone(client.list_shared_arrays().arrays)

    def test_list_public_arrays(self):
        self.assertTrue(len(client.list_public_arrays().arrays) > 0)

    @pytest.mark.udf
    def test_quickstart(self):
        with tiledb.open(
            "tiledb://TileDB-Inc/quickstart_dense", ctx=tiledb.cloud.Ctx()
        ) as A:
            print("quickstart_dense:")
            print(A[:])

        with tiledb.open(
            "tiledb://TileDB-Inc/quickstart_sparse", ctx=tiledb.cloud.Ctx()
        ) as A:
            print("quickstart_sparse:")
            print(A[:])

            with self.assertRaises(TypeError):
                A.apply(None, [(0, 1)])

            import numpy

            orig = A[:]
            self.assertEqual(
                A.apply(lambda x: numpy.sum(x["a"]), [(1, 4), (1, 4)]),
                numpy.sum(orig["a"]),
            )

            orig = A.multi_index[[1, slice(2, 4)], [slice(1, 2), 4]]
            self.assertEqual(
                A.apply(lambda x: numpy.sum(x["a"]), [[1, slice(2, 4)], [(1, 2), 4]]),
                numpy.sum(orig["a"]),
            )

            # v2 UDFs
            orig = A[:]
            self.assertEqual(
                A.apply(lambda x: numpy.sum(x["a"]), [(1, 4), (1, 4)], v2=True),
                numpy.sum(orig["a"]),
            )

            orig = A.multi_index[[1, slice(2, 4)], [slice(1, 2), 4]]
            self.assertEqual(
                A.apply(
                    lambda x: numpy.sum(x["a"]),
                    [[1, slice(2, 4)], [(1, 2), 4]],
                    v2=True,
                ),
                numpy.sum(orig["a"]),
            )

    @pytest.mark.udf
    def test_quickstart_arbitrary_parameters(self):
        with tiledb.open(
            "tiledb://TileDB-Inc/quickstart_sparse", ctx=tiledb.cloud.Ctx()
        ) as A:
            print("quickstart_sparse:")
            print(A[:])

            def hello(data_ignored, param=""):
                return "hello " + param

            self.assertEqual(
                A.apply(hello, [[1, slice(2, 4)], [(1, 2), 4]], v2=True, param="world"),
                "hello world",
            )

    @pytest.mark.udf
    def test_quickstart_async(self):
        with tiledb.open(
            "tiledb://TileDB-Inc/quickstart_dense", ctx=tiledb.cloud.Ctx()
        ) as A:
            print("quickstart_dense:")
            print(A[:])

        with tiledb.open(
            "tiledb://TileDB-Inc/quickstart_sparse", ctx=tiledb.cloud.Ctx()
        ) as A:
            print("quickstart_sparse:")
            print(A[:])

            with self.assertRaises(TypeError):
                A.apply_async(None, [(0, 1)]).get()

            import numpy

            orig = A[:]
            self.assertEqual(
                A.apply_async(lambda x: numpy.sum(x["a"]), [(1, 4), (1, 4)]).get(),
                numpy.sum(orig["a"]),
            )

            orig = A.multi_index[[1, slice(2, 4)], [slice(1, 2), 4]]
            task_name = "test_quickstart_async"
            self.assertEqual(
                A.apply_async(
                    lambda x: numpy.sum(x["a"]),
                    [[1, slice(2, 4)], [(1, 2), 4]],
                    task_name=task_name,
                ).get(),
                numpy.sum(orig["a"]),
            )
            # Validate task name was set
            self.assertEqual(tiledb.cloud.last_udf_task().name, task_name)

            # v2 UDFs
            orig = A[:]
            self.assertEqual(
                A.apply_async(
                    lambda x: numpy.sum(x["a"]), [(1, 4), (1, 4)], v2=True
                ).get(),
                numpy.sum(orig["a"]),
            )

            orig = A.multi_index[[1, slice(2, 4)], [slice(1, 2), 4]]
            task_name = "test_quickstart_async_v2"
            self.assertEqual(
                A.apply_async(
                    lambda x: numpy.sum(x["a"]),
                    [[1, slice(2, 4)], [(1, 2), 4]],
                    task_name=task_name,
                    v2=True,
                ).get(),
                numpy.sum(orig["a"]),
            )

            # Test empty list on second dimension
            orig = A.multi_index[[1, slice(2, 4)], :]
            task_name = "test_quickstart_async_v2"
            self.assertEqual(
                A.apply_async(
                    lambda x: numpy.sum(x["a"]),
                    [[1, slice(2, 4)], []],
                    task_name=task_name,
                    v2=True,
                ).get(),
                numpy.sum(orig["a"]),
            )

            # Test empty tuple on second dimension
            orig = A.multi_index[[1, slice(2, 4)], :]
            task_name = "test_quickstart_async_v2"
            self.assertEqual(
                A.apply_async(
                    lambda x: numpy.sum(x["a"]),
                    [[1, slice(2, 4)], ()],
                    task_name=task_name,
                    v2=True,
                ).get(),
                numpy.sum(orig["a"]),
            )

            # Test None on second dimension
            orig = A.multi_index[[1, slice(2, 4)], :]
            task_name = "test_quickstart_async_v2"
            self.assertEqual(
                A.apply_async(
                    lambda x: numpy.sum(x["a"]),
                    [[1, slice(2, 4)], None],
                    task_name=task_name,
                    v2=True,
                ).get(),
                numpy.sum(orig["a"]),
            )

            # Validate task name was set
            self.assertEqual(tiledb.cloud.last_udf_task().name, task_name)

    def test_quickstart_sql_async(self):
        with tiledb.open(
            "tiledb://TileDB-Inc/quickstart_sparse", ctx=tiledb.cloud.Ctx()
        ) as A:
            print("quickstart_sparse:")
            print(A[:])

            with self.assertRaises(TypeError):
                A.apply(None, [(0, 1)]).get()

            import numpy

            orig = A[:]
            task_name = "test_quickstart_sql_async"
            self.assertEqual(
                int(
                    tiledb.cloud.sql.exec_async(
                        """
                            select sum(a) as sum
                            from `tiledb://TileDB-Inc/quickstart_sparse`
                        """,
                        task_name=task_name,
                    ).get()["sum"]
                ),
                numpy.sum(orig["a"]),
            )

            # Validate task name was set
            self.assertEqual(tiledb.cloud.last_sql_task().name, task_name)

            orig = A.multi_index[[1, slice(2, 4)], [slice(1, 2), 4]]
            self.assertEqual(
                int(
                    tiledb.cloud.sql.exec_async(
                        """
                        select sum(a) as sum
                        from `tiledb://TileDB-Inc/quickstart_sparse`
                        WHERE (`rows`, `cols`) in ((1,1), (2,4))
                        """
                    ).get()["sum"]
                ),
                numpy.sum(orig["a"]),
            )

    def test_context(self):
        with self.assertRaises(ValueError):
            tiledb.cloud.Ctx({"rest.server_address": "1.1.1.1"})

        test_cache_size = str(int(3.14159 * 100000))
        ctx = tiledb.cloud.Ctx({"sm.tile_cache_size": test_cache_size})
        self.assertEqual(ctx.config()["sm.tile_cache_size"], test_cache_size)

    def test_bogus_task_fetch_fails(self):
        with self.assertRaises(tiledb_cloud_error.TileDBCloudError):
            tasks.fetch_results(uuid.uuid4())

    def test_timeout(self):
        def test(_):
            import time

            time.sleep(10)

        with self.assertRaises(tiledb_cloud_error.TileDBCloudError):
            with tiledb.open(
                "tiledb://TileDB-Inc/quickstart_sparse", ctx=tiledb.cloud.Ctx()
            ) as A:
                A.apply_async(test, [(1, 4), (1, 4)], timeout=1).get()

    @pytest.mark.udf
    def test_empty_arrow(self):
        def test():
            import pyarrow

            return pyarrow.Table.from_pydict({})

        tbl = tiledb.cloud.udf.exec(test, result_format="arrow")
        self.assertIsInstance(tbl, pyarrow.Table)

    def test_parse_ranges(self):
        parse_ranges = array.parse_ranges

        a = [1]
        b = [[1, 1]]
        self.assertEqual(parse_ranges(a), json_safe.Value(b))

        a = [1, 2]
        b = [[1, 1], [2, 2]]
        self.assertEqual(parse_ranges(a), json_safe.Value(b))

        a = [[1, 2], 3]
        b = [[1, 1, 2, 2], [3, 3]]
        self.assertEqual(parse_ranges(a), json_safe.Value(b))

        # tuples
        a = [1, (1, 2)]
        b = [[1, 1], [1, 2]]
        self.assertEqual(parse_ranges(a), json_safe.Value(b))

        a = [1, [(1, 2)]]
        b = [[1, 1], [1, 2]]
        self.assertEqual(parse_ranges(a), json_safe.Value(b))

        a = [1, [slice(1, 2)]]
        b = [[1, 1], [1, 2]]
        self.assertEqual(parse_ranges(a), json_safe.Value(b))

        a = [1, slice(2, 3)], [(1, 2), 4]
        b = [[1, 1, 2, 3], [1, 2, 4, 4]]
        self.assertEqual(parse_ranges(a), json_safe.Value(b))

        a = [
            [
                (
                    numpy.datetime64("2012-02-02", "D"),
                    numpy.datetime64("2020-12-31", "D"),
                ),
                numpy.datetime64("2040-06-06", "D"),
            ],
            (
                numpy.datetime64("2012-02-02", "ns"),
                numpy.datetime64("2020-12-31", "ns"),
            ),
        ]
        b = [[15372, 18627, 25724, 25724], [1328140800000000000, 1609372800000000000]]
        self.assertEqual(parse_ranges(a), json_safe.Value(b))

        a = [
            [
                (
                    numpy.datetime64("2012-02-02", "D"),
                    numpy.datetime64("2020-12-31", "D"),
                ),
                numpy.datetime64("2040-06-06", "D"),
            ],
            (
                numpy.datetime64("2012-02-02", "ns"),
                numpy.datetime64("2020-12-31", "ns"),
            ),
        ]
        b = [[15372, 18627, 25724, 25724], [1328140800000000000, 1609372800000000000]]
        self.assertEqual(parse_ranges(a), json_safe.Value(b))

        a = [
            [
                (
                    numpy.timedelta64("2012", "Y"),
                    numpy.timedelta64("2020", "Y"),
                ),
                numpy.timedelta64("6", "D"),
            ],
            (
                numpy.timedelta64(1000000000 * 60 * 24, "ns"),
                numpy.timedelta64(1000000000 * 60 * 24 * 5, "ns"),
            ),
        ]
        b = [[2012, 2020, 6, 6], [1440000000000, 7200000000000]]
        self.assertEqual(parse_ranges(a), json_safe.Value(b))

        start = numpy.datetime64("2019-07-01T00:00:00")
        end = numpy.datetime64("2019-08-01T23:59:59")
        weeks = numpy.arange(start, end, np.timedelta64(1, "W"))
        a = [weeks[0], weeks[1]]
        b = [[1561939200, 1561939200], [1562544000, 1562544000]]
        self.assertEqual(parse_ranges(a), json_safe.Value(b))

        a = [None, [(1, 2), 4]]
        b = [[], [1, 2, 4, 4]]
        self.assertEqual(parse_ranges(a), json_safe.Value(b))

        a = [[], [(1, 2), 4]]
        b = [[], [1, 2, 4, 4]]
        self.assertEqual(parse_ranges(a), json_safe.Value(b))

        a = [(), [(1, 2), 4]]
        b = [[], [1, 2, 4, 4]]
        self.assertEqual(parse_ranges(a), json_safe.Value(b))

        a = [[1, 2, 3], [(1, 2), 4]]
        b = [[1, 1, 2, 2, 3, 3], [1, 2, 4, 4]]
        self.assertEqual(parse_ranges(a), json_safe.Value(b))

        with self.assertRaises(ValueError):
            parse_ranges(["idx"])

    def test_groups(self):
        self.needsUnittestUser()
        got = client.list_groups(
            per_page=2,
            page=4,
        )
        self.assertEqual(2, len(got.groups))

    def test_public_groups(self):
        got = client.list_public_groups(
            namespace="tiledb-inc",
            per_page=3,
            page=2,
        )
        self.assertEqual(3, len(got.groups))
        self.assertEqual(2, got.pagination_metadata.page)
        self.assertEqual(3, got.pagination_metadata.per_page)
        self.assertEqual(3, len(got.groups))

    def test_shared_groups(self):
        self.needsUnittestUser()
        got = client.list_shared_groups(
            per_page=1,
            page=1,
        )
        self.assertEqual(0, len(got.groups))

    def needsUnittestUser(self):
        """Skips the test unless it is run as the ``unittest`` user."""
        if not testonly.is_unittest_user():
            self.skipTest("May fail with non-unittest users.")


@pytest.fixture(scope="function")
def with_metadata_checker(monkeypatch):
    """Intercept requests to arrays and groups list endpoints and checks the URLs."""

    def fake_and_check_request(self, method, url, *args, **kwargs):
        assert "with_metadata=True" in url
        # Return a dummy response.
        return urllib3.response.HTTPResponse(
            b"[]", status=200, retries=urllib3.Retry(history=[])
        )

    monkeypatch.setattr("urllib3.PoolManager.urlopen", fake_and_check_request)


def test_list_arrays_with_metadata_request(with_metadata_checker):
    """with_metadata option is conveyed to the outgoing HTTP request."""
    client.list_arrays(with_metadata=True)


def test_list_public_arrays_with_metadata_request(with_metadata_checker):
    """with_metadata option is conveyed to the outgoing HTTP request."""
    client.list_public_arrays(with_metadata=True)


def test_list_groups_with_metadata_request(with_metadata_checker):
    """with_metadata option is conveyed to the outgoing HTTP request."""
    client.list_groups(with_metadata=True)


def test_list_public_groups_with_metadata_request(with_metadata_checker):
    """with_metadata option is conveyed to the outgoing HTTP request."""
    client.list_public_groups(with_metadata=True)
