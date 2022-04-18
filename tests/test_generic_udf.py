import unittest

import numpy as np
import urllib3

import tiledb.cloud
from tiledb.cloud import client
from tiledb.cloud import config
from tiledb.cloud import testonly
from tiledb.cloud import tiledb_cloud_error
from tiledb.cloud import udf
from tiledb.cloud import utils
from tiledb.cloud.rest_api import models


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

    def test_stored_results_manually(self):
        def show(*args, **kwargs):
            """Function created to call by name in unit tests."""
            return f"called with {args!r} {kwargs!r}"

        with testonly.register_udf(show) as udf_name:
            first = udf.exec_base(
                udf_name,
                1,
                store_results=True,
            )
            second = udf.exec_base(
                udf_name,
                param="two",
                result_format=models.ResultFormat.JSON,
                store_results=True,
            )

            params = (
                # args.
                (first.to_stored_param(),),
                # kwargs.
                dict(named=second.to_stored_param(), basic="three"),
            )
            pickled = utils.b64_pickle(params)

            udf_req = models.GenericUDF(
                language=models.UDFLanguage.PYTHON,
                result_format=models.ResultFormat.JSON,
                version=utils.PYTHON_VERSION,
                image_name="default",
                udf_info_name=udf_name,
                argument=pickled,
                stored_param_uuids=[str(x.task_id) for x in (first, second)],
            )

            namespace = client.find_organization_or_user_for_default_charges(
                config.user
            )

            response: urllib3.HTTPResponse = client.client.udf_api.submit_generic_udf(
                udf=udf_req,
                namespace=namespace,
                _preload_content=False,
            )
            self.assertEqual(200, response.status)
            self.assertEqual(
                rb'''"called with ('called with (1,) {}',) {'named': \"called with () {'param': 'two'}\", 'basic': 'three'}"''',  # noqa: E501
                response.data,
            )

    def test_timeout(self):
        def test():
            import time

            time.sleep(10)

        with self.assertRaises(tiledb_cloud_error.TileDBCloudError):
            udf.exec(test, timeout=1)
