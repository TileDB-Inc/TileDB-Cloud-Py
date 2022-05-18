import datetime
import operator
import unittest
import uuid
from concurrent import futures
from typing import Optional

import attrs
import numpy
import pyarrow

from tiledb.cloud._common import ordered
from tiledb.cloud.taskgraphs import builder
from tiledb.cloud.taskgraphs import client_executor
from tiledb.cloud.taskgraphs import executor
from tiledb.cloud.taskgraphs import types


class ClientExecutorTestUDFs(unittest.TestCase):
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
        self.assertIsNotNone(exec.node(to_fail).exception(15))
        with self.assertRaises(futures.CancelledError):
            exec.node(failchild).result(1)
        with self.assertRaises(futures.CancelledError):
            exec.node(joined).result(10)
        self.assertIs(executor.Status.CANCELLED, exec.node(joined).status)
        self.assertEqual("the value is really 0.0", exec.node(succeedchild).result(0))
        exec.wait(1)
        self.assertIs(executor.Status.FAILED, exec.status)


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
                'insert into tbl values (1000000, 400, 77, "one"), (-999, 501, 199, null)',
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


class NodeOutputValueReplacerTest(unittest.TestCase):
    def test_no_nodes(self):
        input = {
            "here": "there",
            "up": "down",
            "list": [
                1,
                {
                    "__tdbudf__": "immediate",
                    "format": "json",
                    "base64_data": "Mg==",
                },
                3,
                {
                    "__tdbudf__": "__escape__",
                    "__escape__": {
                        "number": "four",
                        "__tdbudf__": 4,
                    },
                },
            ],
        }
        replacer = client_executor._NodeOutputValueReplacer({})
        output = replacer.visit(input)
        expected = {
            "here": "there",
            "up": "down",
            "list": [1, 2, 3, {"number": "four", "__tdbudf__": 4}],
        }
        self.assertEqual(expected, output)

    def test_nodes(self):
        input = [
            None,
            1,
            {
                "__tdbudf__": "immediate",
                "format": "bytes",
                "base64_data": "dGVzdF9ub2Rlcw==",
            },
            {
                "__tdbudf__": "__escape__",
                "__escape__": {
                    "eights": 888,
                    "__tdbudf__": {
                        "__tdbudf__": "node_output",
                        "client_node_id": "88888888-8888-8888-8888-888888888888",
                    },
                },
            },
        ]
        replacer = client_executor._NodeOutputValueReplacer(
            {
                uuid.UUID("88888888-8888-8888-8888-888888888888"): _TestNode(
                    uuid.UUID("99999999-9999-9999-9999-999999999999")
                ),
            }
        )
        output = replacer.visit(input)
        expected = [
            None,
            1,
            b"test_nodes",
            {
                "eights": 888,
                "__tdbudf__": "result of 99999999-9999-9999-9999-999999999999",
            },
        ]
        self.assertEqual(expected, output)


class UDFParamReplacerTest(unittest.TestCase):
    def test_no_nodes(self):
        input = {
            "here": "there",
            "up": "down",
            "list": [
                {"__tdbudf__": "bogus"},
                {
                    "__tdbudf__": "__escape__",
                    "__escape__": {"__tdbudf__": [True, False]},
                },
            ],
        }
        replacer = client_executor._UDFParamReplacer(
            {}, client_executor._ParamFormat.STORED_PARAMS
        )
        output = replacer.visit(input)
        self.assertEqual(input, output)
        self.assertEqual(replacer.seen_nodes, ordered.Set())

    def test_with_nodes(self):
        input = {
            "here": "there",
            "first": {
                "__tdbudf__": "node_output",
                "client_node_id": "aaaaaaaa-bbbb-cccc-dddd-eeeeeeeeeeee",
            },
            "second": [
                {
                    "__tdbudf__": "__escape__",
                    "__escape__": {
                        "__tdbudf__": "value",
                        "dont_visit": {
                            "__tdbudf__": "bogus",
                            "value": {"__tdbudf__": "node_output"},
                        },
                        "do_visit": {
                            "__tdbudf__": "node_output",
                            "client_node_id": "00000000-1111-2222-3333-444444444444",
                        },
                    },
                },
            ],
        }

        expected = {
            "here": "there",
            "first": (
                "encoded 55555555-5555-5555-5555-555555555555 "
                "in _ParamFormat.STORED_PARAMS"
            ),
            "second": [
                {
                    "__tdbudf__": "__escape__",
                    "__escape__": {
                        "__tdbudf__": "value",
                        "dont_visit": {
                            "__tdbudf__": "bogus",
                            "value": {"__tdbudf__": "node_output"},
                        },
                        "do_visit": (
                            "encoded ffffffff-ffff-ffff-ffff-ffffffffffff "
                            "in _ParamFormat.STORED_PARAMS"
                        ),
                    },
                },
            ],
        }
        visitor = client_executor._UDFParamReplacer(
            {
                uuid.UUID("aaaaaaaa-bbbb-cccc-dddd-eeeeeeeeeeee"): _TestNode(
                    uuid.UUID("55555555-5555-5555-5555-555555555555")
                ),
                uuid.UUID("00000000-1111-2222-3333-444444444444"): _TestNode(
                    uuid.UUID("ffffffff-ffff-ffff-ffff-ffffffffffff")
                ),
            },
            client_executor._ParamFormat.STORED_PARAMS,
        )
        self.assertEqual(expected, visitor.visit(input))
        self.assertEqual(
            ordered.Set(
                (
                    _TestNode(uuid.UUID("55555555-5555-5555-5555-555555555555")),
                    _TestNode(uuid.UUID("ffffffff-ffff-ffff-ffff-ffffffffffff")),
                )
            ),
            visitor.seen_nodes,
        )

    def test_small(self):
        input = {
            "__tdbudf__": "node_output",
            "client_node_id": "99999999-9999-9999-9999-999999999999",
        }

        visitor = client_executor._UDFParamReplacer(
            {
                uuid.UUID("99999999-9999-9999-9999-999999999999"): _TestNode(
                    uuid.UUID("33333333-3333-3333-3333-333333333333")
                )
            },
            client_executor._ParamFormat.VALUES,
        )
        expected = "encoded 33333333-3333-3333-3333-333333333333 in _ParamFormat.VALUES"
        self.assertEqual(expected, visitor.visit(input))
        self.assertEqual(
            ordered.Set([_TestNode(uuid.UUID("33333333-3333-33333333--333333333333"))]),
            visitor.seen_nodes,
        )


@attrs.define(frozen=True, slots=True)
class _TestNode:
    """A dummy class which implements just what the visitors use."""

    _task_id: Optional[uuid.UUID] = None

    def result(self, timeout=None):
        return f"result of {self._task_id}"

    def _encode_for_param(self, mode):
        return f"encoded {self._task_id} in {mode}"

    def task_id(self):
        return self._task_id
