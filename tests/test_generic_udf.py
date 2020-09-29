import os
import unittest

import numpy as np
from tiledb.cloud import udf
import tiledb.cloud

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


class RegisteredUDFTest(unittest.TestCase):
    def test_register_generic_udf(self):
        def test_register_me(arg, kwarg1=None):
            if kwarg1:
                return kwarg1
            else:
                return arg

        udf.register_generic_udf(test_register_udf, "registered_generic_udf")

        res = udf.exec("test arg", func="unittest/registered_generic_udf")
        self.assertEqual(res, "test arg")

        res = udf.exec(kwarg1="test kwarg1", func="unittest/registered_generic_udf")
        self.assertEqual(res, "test kwarg1")
