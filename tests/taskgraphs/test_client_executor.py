import datetime
import operator
import tempfile
import time
import unittest

import numpy
import pyarrow

from tiledb.cloud._common import futures
from tiledb.cloud.taskgraphs import builder
from tiledb.cloud.taskgraphs import client_executor
from tiledb.cloud.taskgraphs import executor
from tiledb.cloud.taskgraphs import types


class ClientExecutorTestUDFs(unittest.TestCase):
    def test_empty(self):
        grf = builder.TaskGraphBuilder("empty")
        exec = client_executor.LocalExecutor(grf, name="empty")
        exec.execute()
        exec.wait(1)
        self.assertIs(executor.Status.SUCCEEDED, exec.status)

    def test_one(self):
        grf = builder.TaskGraphBuilder("test_one")
        len_node = grf.udf(len, types.args("some string"), result_format="json")

        exec = client_executor.LocalExecutor(grf, name="test_one exec")
        exec.execute()
        len_exec = exec.node(len_node)
        self.assertEqual(11, len_exec.result(15))
        exec.wait(1)
        self.assertIs(executor.Status.SUCCEEDED, exec.status)

    def test_two(self):
        grf = builder.TaskGraphBuilder("test_two")
        first = grf.udf(lambda: 10)
        out = grf.udf("my value is {!r}".format, types.args(first))

        exec = client_executor.LocalExecutor(grf, name="test_two exec")
        exec.execute()
        self.assertEqual("my value is 10", exec.node(out).result(15))
        self.assertEqual(10, exec.node(first).result(0))
        exec.wait(1)
        self.assertIs(executor.Status.SUCCEEDED, exec.status)

    def test_split_join(self):
        grf = builder.TaskGraphBuilder("test_diamond")
        top = grf.udf(lambda: "step on ", name="word")
        reverser = grf.udf(lambda val: val[::-1], types.args(top), name="reverser")
        join = grf.udf(operator.add, types.args(top, reverser), name="together")

        exec = client_executor.LocalExecutor(grf, name="test_diamond exec")
        exec.execute()
        self.assertEqual("step on  no pets", exec.node(join).result(30))

    def test_failure(self):
        grf = builder.TaskGraphBuilder("test_failure")
        to_fail = grf.udf(lambda: 1 / 0, name="div0")
        failchild = grf.udf(
            "the value is {}".format, types.args(to_fail), name="failchild"
        )
        to_succeed = grf.udf(lambda: 0 / 1, name="zero")
        succeedchild = grf.udf(
            "the value is really {}".format, types.args(to_succeed), name="succeedchild"
        )
        joined = grf.udf(
            (lambda a, b: (a, b)), types.args(failchild, succeedchild), name="join"
        )

        exec = client_executor.LocalExecutor(grf, name="test_failure exec")
        exec.execute()
        self.assertEqual(0, exec.node(to_succeed).result(15))
        tf_exc = exec.node(to_fail).exception(15)
        self.assertIsNotNone(tf_exc)
        with self.assertRaises(executor.ParentFailedError) as fccm:
            exec.node(failchild).result(1)
        self.assertIs(fccm.exception.node, exec.node(to_fail))
        self.assertIs(fccm.exception.cause, tf_exc)
        with self.assertRaises(executor.ParentFailedError) as jcm:
            exec.node(joined).result(1)
        self.assertIs(jcm.exception.node, exec.node(to_fail))
        self.assertIs(jcm.exception.cause, tf_exc)
        self.assertIs(executor.Status.PARENT_FAILED, exec.node(joined).status)
        self.assertEqual("the value is really 0.0", exec.node(succeedchild).result(10))
        exec.wait(10)
        self.assertIs(executor.Status.FAILED, exec.status)


class ClientExecutorTestLocal(unittest.TestCase):
    def test_basic(self):
        grf = builder.TaskGraphBuilder(name="test_local")
        double = grf.udf(lambda x: 2 * x, types.args(2), local=True)

        exec = client_executor.LocalExecutor(grf, name="test_local exec")
        exec.execute()
        double_exec = exec.node(double)
        self.assertEqual(4, double_exec.result(30))
        self.assertIsNone(double_exec.task_id())
        exec.wait(10)

    def test_concurrent(self):
        import os
        import os.path
        import time

        def touch_and_wait(dir, file):
            full_path = os.path.join(dir, file)
            open(full_path, "w").close()
            while os.path.exists(full_path):
                time.sleep(0.01)
            return file

        with tempfile.TemporaryDirectory() as tmpdir:
            grf = builder.TaskGraphBuilder()
            one = grf.udf(touch_and_wait, types.args(tmpdir, "one"), local=True)
            two = grf.udf(touch_and_wait, types.args(tmpdir, "two"), local=True)
            out = grf.udf(" ".join, types.args((one, two)), local=True)
            exec = client_executor.LocalExecutor(grf)
            exec.execute()

            # The touch_and_wait tasks will get stuck in their wait-loop for
            # the file they just created to be deleted, so waiting on the task
            # must necessarily time out.
            with self.assertRaises(futures.TimeoutError):
                exec.node(one).result(1)
            with self.assertRaises(futures.TimeoutError):
                exec.node(two).result(1)

            p_one = os.path.join(tmpdir, "one")
            p_two = os.path.join(tmpdir, "two")

            # Ensure that the tasks have gotten to the point where they *did*
            # create their files.
            while not os.path.exists(p_one):
                time.sleep(0.01)
            while not os.path.exists(p_two):
                time.sleep(0.01)
            # After we remove the files, the tasks will run to completion.
            os.remove(p_one)
            os.remove(p_two)
            self.assertEqual("one two", exec.node(out).result(5))


class ClientExecutorTestArrays(unittest.TestCase):
    def test_basic(self):
        grf = builder.TaskGraphBuilder()
        arr = grf.array_read(
            "tiledb://TileDB-Inc/quickstart_dense",
            raw_ranges=[[1, 1, 2, 4], []],
        )
        grf.udf(lambda x: int(numpy.sum(x["a"])), types.args(arr), name="stringify")

        exec = client_executor.LocalExecutor(grf, name="arrays test_basic")
        exec.execute()
        self.assertEqual(136, exec.node("stringify").result(30))
        exec.wait(5)
        self.assertIs(executor.Status.SUCCEEDED, exec.status)

    def test_two_arrays(self):
        """Verify that we can pass multiple arrays to one UDF node."""
        grf = builder.TaskGraphBuilder()
        dense = grf.array_read(
            "tiledb://TileDB-Inc/quickstart_dense",
            raw_ranges=[[1, 4], []],
        )
        sparse = grf.array_read(
            "tiledb://TileDB-Inc/quickstart_sparse",
            raw_ranges=[[], []],
        )
        sums = grf.udf(
            lambda lst: [int(numpy.sum(x["a"])) for x in lst],
            types.args([dense, {"a": [-1, -2, -3]}, sparse]),
        )
        exec = client_executor.LocalExecutor(grf)
        exec.execute()
        self.assertEqual([136, -6, 6], exec.node(sums).result(30))
        exec.wait(5)
        self.assertIs(executor.Status.SUCCEEDED, exec.status)

    def test_layouts(self):
        grf = builder.TaskGraphBuilder()
        arrs = dict(
            rm=grf.array_read(
                "tiledb://TileDB-Inc/quickstart_dense",
                raw_ranges=[[1, 4], [1, 4]],
                layout="r",
                name="rm",
            ),
            cm=grf.array_read(
                "tiledb://TileDB-Inc/quickstart_dense",
                raw_ranges=[[1, 4], [1, 4]],
                layout=types.Layout.COL_MAJOR,
                name="cm",
            ),
            gl=grf.array_read(
                "tiledb://TileDB-Inc/quickstart_dense",
                raw_ranges=[[1, 4], [1, 4]],
                layout="global-order",
                name="gl",
            ),
        )

        def to_python(arr: "types.ArrayMultiIndex"):
            return arr["a"].tolist()

        pythons = {
            name: grf.udf(to_python, types.args(arr), name=name + " node")
            for name, arr in arrs.items()
        }
        merged = grf.udf(lambda **x: x, types.args(**pythons))

        exec = client_executor.LocalExecutor(grf, name="test_layouts")
        exec.execute()

        self.assertEqual(
            dict(
                rm=[[1, 2, 3, 4], [5, 6, 7, 8], [9, 10, 11, 12], [13, 14, 15, 16]],
                cm=[[1, 5, 9, 13], [2, 6, 10, 14], [3, 7, 11, 15], [4, 8, 12, 16]],
                gl=[[1, 2, 3, 4], [5, 6, 7, 8], [9, 10, 11, 12], [13, 14, 15, 16]],
            ),
            exec.node(merged).result(30),
        )

    def test_node_inputs(self):
        """Tests using the output of other nodes as params for an array read."""
        grf = builder.TaskGraphBuilder()
        uri = grf.udf("tiledb://TileDB-Inc/quickstart_{}".format, types.args("dense"))
        ones = grf.udf(lambda x: [x, x], types.args(1))

        arr = grf.array_read(
            uri,
            raw_ranges=[ones, [1, 4]],
            buffers=grf.udf(lambda: ["a"]),
        )
        summed = grf.udf(lambda x: int(numpy.sum(x["a"])), types.args(arr))
        join = grf.udf(
            "{name}[{ones}, [1, 4]]['a'] -> {sum}".format,
            types.args(name=uri, ones=ones, sum=summed),
        )
        exec = client_executor.LocalExecutor(grf)
        exec.execute()
        self.assertEqual(
            "tiledb://TileDB-Inc/quickstart_dense[[1, 1], [1, 4]]['a'] -> 10",
            exec.node(join).result(30),
        )
        exec.wait(5)

    def test_array_split(self):
        """Tests using a single array-read node in multiple downstream UDFs."""
        grf = builder.TaskGraphBuilder()
        arr = grf.array_read(
            "tiledb://TileDB-Inc/quickstart_sparse",
            raw_ranges=[[], []],
        )
        summed = grf.udf(lambda x: int(numpy.sum(x["a"])), types.args(arr))
        avgd = grf.udf(lambda x: float(numpy.average(x["a"])), types.args(arr))

        exec = client_executor.LocalExecutor(grf)
        exec.execute()
        self.assertEqual(6, exec.node(summed).result(30))
        self.assertEqual(2.0, exec.node(avgd).result(30))
        exec.wait(5)


class ClientExecutorTestSQLs(unittest.TestCase):
    def test_basic(self):
        grf = builder.TaskGraphBuilder()
        sql = grf.sql(
            "select sum(a) as sum from `tiledb://TileDB-Inc/quickstart_sparse`",
            name="quickstart_sparse",
        )

        exec = client_executor.LocalExecutor(grf)
        exec.execute()
        result_table = exec.node(sql).result(30)
        self.assertIsInstance(result_table, pyarrow.Table)
        self.assertEqual({"sum": [6]}, result_table.to_pydict())
        exec.wait(5)

    def test_params(self):
        grf = builder.TaskGraphBuilder()
        sql = grf.sql(
            "select * from tbl where ? < intcol",
            init_commands=[
                """create temporary table tbl
                    (intcol int4, floatcol double, uintcol int8 unsigned, strcol text)
                """,
                'insert into tbl values (1000000, 400, 77, "one"), (-999, 501, 199, null)',  # noqa: E501
            ],
            parameters=[0],
            result_format="json",
        )

        grf.udf(repr, types.args(sql), name="output", result_format="json")

        exec = client_executor.LocalExecutor(grf)
        exec.execute()
        self.assertEqual(
            [{"floatcol": 400, "intcol": 1000000, "strcol": "one", "uintcol": 77}],
            exec.node(sql).result(30),
        )
        self.assertEqual(
            "[{'floatcol': 400, 'intcol': 1000000, 'strcol': 'one', 'uintcol': 77}]",
            exec.node("output").result(30),
        )
        exec.wait(5)

    def test_node_inputs(self):
        grf = builder.TaskGraphBuilder()
        add = grf.udf(lambda: 500)
        grf.sql(
            "select sum(a + ?) + ? a from `tiledb://TileDB-Inc/quickstart_sparse`",
            parameters=[add, 7],
            name="sql",
        )
        exec = client_executor.LocalExecutor(grf)
        exec.execute()
        result_table = exec.node("sql").result(30)
        self.assertIsInstance(result_table, pyarrow.Table)
        self.assertEqual({"a": [1513]}, result_table.to_pydict())
        exec.wait(5)


class ClientExecutorTestInputs(unittest.TestCase):
    maxDiff = None

    def test_basic(self):
        grf = builder.TaskGraphBuilder()
        start = grf.input("start")
        period = grf.input("period", datetime.timedelta(hours=24))

        added = grf.udf(operator.add, types.args(start, period), name="added")
        result = grf.udf(
            "{start:%Y-%m-%d %H:%M:%S%z} + {period} = {sum:%Y-%m-%d %H:%M:%S%z}".format,
            types.args(start=start, period=period, sum=added),
        )

        exec_def = client_executor.LocalExecutor(grf)
        with self.assertRaisesRegex(TypeError, "missing 1 required"):
            exec_def.execute()
        with self.assertRaisesRegex(TypeError, "unexpected arguments"):
            exec_def.execute(start=None, bogus=...)

        exec_def.execute(
            start=datetime.datetime(2010, 6, 21, 0, 30, tzinfo=datetime.timezone.utc)
        )
        self.assertEqual(
            datetime.datetime(2010, 6, 22, 0, 30, tzinfo=datetime.timezone.utc),
            exec_def.node("added").result(30),
        )
        self.assertEqual(
            "2010-06-21 00:30:00+0000 + 1 day, 0:00:00 = 2010-06-22 00:30:00+0000",
            exec_def.node(result).result(30),
        )
        exec_def.wait(5)
        self.assertEqual(executor.Status.SUCCEEDED, exec_def.status)

        exec_non_def = client_executor.LocalExecutor(grf)
        exec_non_def.execute(
            start=datetime.datetime(
                2022, 5, 17, 19, tzinfo=datetime.timezone(datetime.timedelta(hours=-4))
            ),
            period=datetime.timedelta(hours=3, minutes=45, seconds=6),
        )
        self.assertEqual(
            "2022-05-17 19:00:00-0400 + 3:45:06 = 2022-05-17 22:45:06-0400",
            exec_non_def.node(result).result(30),
        )
        exec_def.wait(5)
        exec_non_def.wait(5)

    def test_node_inputs(self):
        grf = builder.TaskGraphBuilder()
        uri = grf.input("uri", "tiledb://TileDB-Inc/quickstart_dense")
        frm = grf.input("frm")
        to = grf.input("to")

        arr = grf.array_read(uri, raw_ranges=[[], [frm, to]])
        query = grf.sql(
            """
                select * from `tiledb://TileDB-Inc/quickstart_dense`
                where ? <= `cols` and `cols` <= ?
            """,
            parameters=(frm, to),
            result_format="json",
        )

        def make_nice(arr, sql_result):
            nice_arr = {k: v.tolist() for k, v in arr.items()}
            return nice_arr, sql_result

        result = grf.udf(make_nice, types.args(arr, query))

        exec = client_executor.LocalExecutor(grf)
        exec.execute(frm=2, to=3)
        self.assertEqual(
            (
                {
                    "a": [[2, 3], [6, 7], [10, 11], [14, 15]],
                    "cols": [[2, 3], [2, 3], [2, 3], [2, 3]],
                    "rows": [[1, 1], [2, 2], [3, 3], [4, 4]],
                },
                [
                    dict(a=2, cols=2, rows=1),
                    dict(a=3, cols=3, rows=1),
                    dict(a=6, cols=2, rows=2),
                    dict(a=7, cols=3, rows=2),
                    dict(a=10, cols=2, rows=3),
                    dict(a=11, cols=3, rows=3),
                    dict(a=14, cols=2, rows=4),
                    dict(a=15, cols=3, rows=4),
                ],
            ),
            exec.node(result).result(30),
        )
        exec.wait(5)


class ClientExecutorTestEnvironment(unittest.TestCase):
    def test_timeout(self):
        grf = builder.TaskGraphBuilder(name="test_timeout")
        slept = grf.udf(
            time.sleep,
            types.args(15),
            timeout=datetime.timedelta(seconds=5),
        )
        exec = client_executor.LocalExecutor(grf)
        exec.execute()
        with self.assertRaises(Exception):
            exec.node(slept).result(30)
        self.assertIs(client_executor.Status.FAILED, exec.node(slept).status)

    def test_resource_class(self):
        def big_sum():
            # An experimentally determined value where reifying the sequence
            # is too much for a normal-sized UDF, but fine for a large UDF.
            # Tune (or replace with a better implementation) as needed.
            nums = tuple(range(128 * 1024**2))
            return sum(nums)

        grf = builder.TaskGraphBuilder(name="test_resource_class")
        small = grf.udf(big_sum)
        big = grf.udf(big_sum, resource_class="large")
        exec = client_executor.LocalExecutor(grf)
        exec.execute()

        with self.assertRaises(Exception):
            exec.node(small).result(30)
        self.assertIs(client_executor.Status.FAILED, exec.node(small).status)
        self.assertEqual(9007199187632128, exec.node(big).result(30))
