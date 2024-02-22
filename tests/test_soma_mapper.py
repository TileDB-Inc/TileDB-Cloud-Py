import sys
import unittest

import tiledb.cloud
import tiledb.cloud.soma


class SOMAMapperTest(unittest.TestCase):
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
