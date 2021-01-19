import tiledb, tiledb.cloud
import sys, os, platform, unittest
import numpy as np
from tiledb.cloud import client
from tiledb.cloud import array
from tiledb.cloud import tasks
from tiledb.cloud import tiledb_cloud_error

tiledb.cloud.login(
    token=os.environ["TILEDB_CLOUD_HELPER_VAR"],
    host=os.environ.get("TILEDB_CLOUD_REST_HOST", None),
)


class ResultsRetrievalTests(unittest.TestCase):
    def test_sql_task_result_retrieval(self):
        with tiledb.open(
            "tiledb://TileDB-Inc/quickstart_sparse", ctx=tiledb.cloud.Ctx()
        ) as A:
            print("quickstart_sparse:")
            print(A[:])

            with self.assertRaises(TypeError):
                A.apply(None, [(0, 1)]).get()

            import numpy

            orig = A[:]
            task_name = "test_quickstart_sql_retrieval"
            tiledb.cloud.sql.exec_async(
                "select sum(a) as sum from `tiledb://TileDB-Inc/quickstart_sparse`",
                task_name=task_name,
                store_results=True,
            )

            # Validate we can retrieve last sql task's results
            task = tiledb.cloud.last_sql_task()
            self.assertEqual(task.name, task_name)

            sql_res_from_retrieval = tiledb.cloud.task_results(task.id)

            self.assertEqual(
                int(sql_res_from_retrieval["sum"]),
                numpy.sum(orig["a"]),
            )

    def test_array_udf_task_result_retrieval(self):
        with tiledb.open(
            "tiledb://TileDB-Inc/quickstart_sparse", ctx=tiledb.cloud.Ctx()
        ) as A:
            print("quickstart_sparse:")
            print(A[:])

            with self.assertRaises(TypeError):
                A.apply(None, [(0, 1)]).get()

            import numpy

            orig = A[:]
            task_name = "test_quickstart_array_udf_retrieval"
            A.apply(
                lambda x: numpy.sum(x["a"]),
                [(1, 4), (1, 4)],
                task_name=task_name,
                store_results=True,
            )

            task = tiledb.cloud.last_udf_task()
            self.assertEqual(task.name, task_name)

            array_udf_res_from_retrieval = tiledb.cloud.task_results(task.id)

            self.assertEqual(
                int(array_udf_res_from_retrieval),
                numpy.sum(orig["a"]),
            )

    def test_generic_udf_task_result_retrieval(self):
        with tiledb.open(
            "tiledb://TileDB-Inc/quickstart_sparse", ctx=tiledb.cloud.Ctx()
        ) as A:
            print("quickstart_sparse:")
            print(A[:])

            with self.assertRaises(TypeError):
                A.apply(None, [(0, 1)]).get()

            task_name = "test_generic_udf_retrieval"

            def ten():
                return 10

            tiledb.cloud.udf.exec(ten, task_name=task_name, store_results=True)

            task = tiledb.cloud.last_udf_task()
            self.assertEqual(task.name, task_name)

            array_udf_res_from_retrieval = tiledb.cloud.task_results(task.id)

            self.assertEqual(int(array_udf_res_from_retrieval), 10)
