import random
import string
import time
import unittest

from tiledb.cloud import rest_api
from tiledb.cloud import testonly
from tiledb.cloud.taskgraphs import builder
from tiledb.cloud.taskgraphs import registration
from tiledb.cloud.taskgraphs import types


class RegistrationTest(unittest.TestCase):
    maxDiff = None

    def test_register(self):
        name = testonly.random_name("registered_graph")
        grf = builder.TaskGraphBuilder(name=name)
        original = grf._tdb_to_json()

        try:
            registration.register(grf)
            time.sleep(1)
            loaded = registration.load(name)
            self.assertEqual(original["nodes"], loaded["nodes"])

            arr_node = grf.array_read(
                "tiledb://something/else",
                raw_ranges=[[1, 2], [3, 4]],
                layout="c",
            )
            grf.udf(
                repr,
                types.args(arr_node),
                name="ooga",
                result_format="booga",
                image_name="monkey",
            )
            updated = grf._tdb_to_json()
            registration.update(grf)
            time.sleep(1)

            updated_loaded = registration.load(name)
            self.assertEqual(updated["nodes"], updated_loaded["nodes"])

        finally:
            registration.delete(name)

        with self.assertRaises(rest_api.ApiException):
            registration.load(name)

    def test_rename(self):
        old_name = f"zzz_unittest_manual_{random_letters(10)}"

        grf = builder.TaskGraphBuilder(old_name)
        current_name = old_name

        try:
            registration.register(grf)

            new_name = f"{old_name}_renamed"
            new_grf = builder.TaskGraphBuilder(new_name)
            registration.update(new_grf, old_name)
            current_name = new_name
            registration.load(new_name)
        finally:
            registration.delete(current_name)


def random_letters(n: int) -> str:
    return "".join(random.choices(string.ascii_letters, k=n))
