import os
import unittest

import numpy as np

import tiledb.cloud
from tiledb.cloud import testonly
from tiledb.cloud import udf

tiledb.cloud.login(
    token=os.environ["TILEDB_CLOUD_HELPER_VAR"],
    host=os.environ.get("TILEDB_CLOUD_REST_HOST", None),
)


class GenericUDFTest(unittest.TestCase):
    def test_simple_generic_udf(self):
        res = udf.exec(lambda x: np.sum(x), [1, 4, 10, 40])
        self.assertEqual(res, 55)

    def test_kwargs(self):
        def test_func(kw1=None, kw2=None):
            return [kw1, kw2]

        res = udf.exec(test_func, kw1="test")
        self.assertEqual(res, ["test", None])

    def test_positional_args(self):
        def test_func(pos1, pos2, kw1=None, kw2=None):
            return [pos1, pos2, kw1, kw2]

        res = udf.exec(test_func, 1, [2, 2])
        self.assertEqual(res, [1, [2, 2], None, None])

    def test_positional_args_and_kwargs(self):
        def test_func(pos1, pos2, kw1=None, kw2=None):
            return [pos1, pos2, kw1, kw2]

        task_name = "test_positional_args_and_kwargs"
        res = udf.exec(
            test_func,
            pos1=1,
            pos2=[2, 2],
            kw1=dict(test=1),
            kw2=[1, 2, 3],
            task_name=task_name,
        )
        self.assertEqual(res, [1, [2, 2], {"test": 1}, [1, 2, 3]])
        self.assertEqual(tiledb.cloud.last_udf_task().name, task_name)

    def test_pass_by_name(self):
        def show(*args, **kwargs):
            """Function created to call by name in unit tests."""
            return f"called with {args!r} {kwargs!r}"

        with testonly.register_udf(show) as udf_name:
            got = udf.exec(udf_name, 1, 2, 3, easy_as="abc")
        self.assertEqual(got, "called with (1, 2, 3) {'easy_as': 'abc'}")
