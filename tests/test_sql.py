import unittest

import tiledb
import tiledb.cloud


class BasicTests(unittest.TestCase):
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

    def test_sql_init_commands(self):
        task_name = "test_sql_init_commands"
        self.assertEqual(
            int(
                tiledb.cloud.sql.exec_async(
                    "select @A a", task_name=task_name, init_commands=["SET @A=1"]
                ).get()["a"]
            ),
            1,
        )

        # Validate task name was set
        self.assertEqual(tiledb.cloud.last_sql_task().name, task_name)

    def test_sql_parameters(self):
        task_name = "test_sql_parameters"
        self.assertEqual(
            float(
                tiledb.cloud.sql.exec_async(
                    "select @A a, ? param1",
                    task_name=task_name,
                    init_commands=["SET @A=1"],
                    parameters=["1.1"],
                ).get()["param1"]
            ),
            1.1,
        )

        # Validate task name was set
        self.assertEqual(tiledb.cloud.last_sql_task().name, task_name)

    def test_quickstart_sql_arrow(self):
        with tiledb.open(
            "tiledb://TileDB-Inc/quickstart_sparse", ctx=tiledb.cloud.Ctx()
        ) as A:
            print("quickstart_sparse:")
            print(A[:])

            with self.assertRaises(TypeError):
                A.apply(None, [(0, 1)]).get()

            import numpy

            orig = A[:]
            task_name = "test_quickstart_sql_arrow"
            self.assertEqual(
                int(
                    tiledb.cloud.sql.exec_async(
                        """
                            select sum(a) as sum
                            from `tiledb://TileDB-Inc/quickstart_sparse`
                        """,
                        task_name=task_name,
                        result_format=tiledb.cloud.ResultFormat.ARROW,
                    ).get()["sum"]
                ),
                numpy.sum(orig["a"]),
            )

    def test_quickstart_sql_json(self):
        with tiledb.open(
            "tiledb://TileDB-Inc/quickstart_sparse", ctx=tiledb.cloud.Ctx()
        ) as A:
            print("quickstart_sparse:")
            print(A[:])

            with self.assertRaises(TypeError):
                A.apply(None, [(0, 1)]).get()

            import numpy

            orig = A[:]
            task_name = "test_quickstart_sql_arrow"
            self.assertEqual(
                int(
                    tiledb.cloud.sql.exec_async(
                        """
                            select sum(a) as sum
                            from `tiledb://TileDB-Inc/quickstart_sparse`
                        """,
                        task_name=task_name,
                        result_format=tiledb.cloud.ResultFormat.JSON,
                    ).get()["sum"]
                ),
                numpy.sum(orig["a"]),
            )
