import logging
import sys
import unittest

import tiledb.cloud
import tiledb.cloud.soma


class TestSOMAIngestion(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.test_file_path = "s3://tiledb-unittest/soma-ingestion-test/pbmc3k.h5ad"

        (
            cls.namespace,
            cls.storage_path,
            cls.acn,
        ) = tiledb.cloud.groups._default_ns_path_cred()
        cls.namespace = cls.namespace.rstrip("/")
        cls.storage_path = cls.storage_path.rstrip("/")
        cls.array_name = tiledb.cloud._common.testonly.random_name("soma-test")
        cls.destination = (
            f"tiledb://{cls.namespace}/{cls.storage_path}/{cls.array_name}"
        )

        return super().setUpClass()

    # TODO: Allow test to run when VFS access is enabled
    @unittest.skip("Fails until unittest user obtains VFS access.")
    def test_ingest_h5ad(self):
        tiledb.cloud.soma.ingest_h5ad(
            output_uri=self.destination,
            input_uri=self.test_file_path,
            measurement_name="RNA",
            logging_level=logging.DEBUG,
        )

        array_uri = f"tiledb://{self.namespace}/{self.array_name}"
        array_info = tiledb.cloud.array.info(array_uri)
        self.assertEqual(array_info.name, self.array_name)
        self.assertEqual(array_info.namespace, self.namespace)
        tiledb.cloud.array.delete_array(array_uri)

    # TODO: Allow test to run when VFS access is enabled
    @unittest.skip("Fails until unittest user obtains VFS access.")
    def test_ingest_h5ad_dry_run(self):
        with self.assertLogs(level=logging.INFO) as lg:
            tiledb.cloud.soma.ingest_h5ad(
                output_uri=self.destination,
                input_uri=self.test_file_path,
                measurement_name="RNA",
                logging_level=logging.DEBUG,
                dry_run=True,
            )
            self.assertEqual(
                f"Dry run for {self.test_file_path} to {self.destination}", lg.output[0]
            )


class TestSOMAMapper(unittest.TestCase):
    def __init__(self, foo):
        super().__init__(foo)
        self.maxDiff = None

    def test_mapper_basic_realtime(self):
        self._test_mapper_basic(False)

    def test_mapper_basic_batch(self):
        self._test_mapper_basic(True)

    def _test_mapper_basic(self, use_batch_mode):
        if sys.version_info < (3, 8, 0):
            # https://github.com/TileDB-Inc/tiledbsoma-feedstock/pull/86
            return

        soma_collection_uri = "tiledb://unittest/stack-small-soco-prod"
        measurement_name = "RNA"
        if use_batch_mode:
            pass
        else:
            pass

        g = tiledb.cloud.soma.build_collection_mapper_workflow_graph(
            soma_collection_uri=soma_collection_uri,
            measurement_name=measurement_name,
            X_layer_name="data",
            callback=lambda x: x.shape,
            use_batch_mode=False,
            namespace="unittest",
        )

        g.compute()
        g.wait()

        self.assertTrue(g.done())
        self.assertEqual(g.status, tiledb.cloud.dag.status.Status.COMPLETED)

        for k, v in g.nodes_by_name.items():
            self.assertEqual(v.status, tiledb.cloud.dag.status.Status.COMPLETED)
            print(v.result())

        self.assertEqual(
            g.end_results_by_name(),
            {
                "collector": {
                    "tiledb://unittest/3c0e8956-12d1-463d-87c4-16f644c204c9": [
                        3,
                        5,
                    ],
                    "tiledb://unittest/53109d02-4145-4860-9c86-349bb5b8c588": [
                        3,
                        6,
                    ],
                    "tiledb://unittest/c5cdcdcd-2ce4-4c1d-bed5-b90232568977": [
                        3,
                        5,
                    ],
                    "tiledb://unittest/a0b92925-a0da-41d4-aa55-f9c3e526ff2d": [
                        3,
                        4,
                    ],
                }
            },
        )