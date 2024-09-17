import datetime
import unittest

import numpy as np
import urllib3

import tiledb.cloud
from tiledb.cloud import client
from tiledb.cloud import config
from tiledb.cloud import rest_api
from tiledb.cloud import tiledb_cloud_error
from tiledb.cloud import udf
from tiledb.cloud._common import testonly
from tiledb.cloud._common import utils
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
                config.user, required_action=rest_api.NamespaceActions.RUN_JOB
            )

            response: urllib3.HTTPResponse = client.build(
                rest_api.UdfApi
            ).submit_generic_udf(
                udf=udf_req,
                namespace=namespace,
                _preload_content=False,
            )
            try:
                self.assertEqual(200, response.status)
                self.assertEqual(
                    rb'''"called with ('called with (1,) {}',) {'named': \"called with () {'param': 'two'}\", 'basic': 'three'}"''',  # noqa: E501
                    response.data,
                )
            finally:
                utils.release_connection(response)

    def test_timeout(self):
        def test():
            import time

            time.sleep(10)

        with self.assertRaises(tiledb_cloud_error.TileDBCloudError):
            udf.exec(test, timeout=1)


class ParserTest(unittest.TestCase):
    def test_parse_udf_name_timestamp(self) -> None:
        inouts = (
            ("just-a-name", ("just-a-name", None)),
            ("udf/name@2022-03-04", ("udf/name", _utc(2022, 3, 4))),
            ("other/name@2022-03-04 05:06", ("other/name", _utc(2022, 3, 4, 5, 6))),
            ("prince@1999-09-09 21:21:21", ("prince", _utc(1999, 9, 9, 21, 21, 21))),
            (
                "uses-t@2024-09-17T20:59:59.999999",
                ("uses-t", _utc(2024, 9, 17, 20, 59, 59, 999999)),
            ),
        )
        for inval, outs in inouts:
            with self.subTest(inval):
                self.assertEqual(outs, udf._parse_udf_name_timestamp(inval))

    def test_parse_udf_name_timestamp_bad(self) -> None:
        bads = (
            "name@not a time at all",
            "too-short@2020-01",
            "no-space@2020-01-0203",
            "lowercase-t@2020-01-02t03:04",
            "hour-only@2020-01-02 03",
            "too-precise@2020-01-02 03:04:05.67890123456",
        )
        for bad in bads:
            with self.subTest(bad):
                with self.assertRaises(ValueError):
                    udf._parse_udf_name_timestamp(bad)


def _utc(*args: int) -> datetime.datetime:
    return datetime.datetime(*args, tzinfo=datetime.timezone.utc)
