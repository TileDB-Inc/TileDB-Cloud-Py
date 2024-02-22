import unittest

import tiledb.cloud
import tiledb.cloud.soma


class SOMAMapperTest(unittest.TestCase):
    def test_mapper_basic_realtime(self):
        self._test_mapper_basic(False)

    def test_mapper_basic_batch(self):
        self._test_mapper_basic(True)

    def _test_mapper_basic(self, use_batch_mode):
        soma_collection_uri = "tiledb://TileDB-Inc/stack-small-soco-prod"
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
            namespace="TileDB-Inc",
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
                    "tiledb://TileDB-Inc/432fa76f-34a0-4ed7-b0cb-69d6c137b208": [3, 5],
                    "tiledb://TileDB-Inc/a719e2b5-69e6-4818-a831-f76a6b4c95de": [3, 6],
                    "tiledb://TileDB-Inc/042bee7b-a91a-427f-b932-36787baff2eb": [3, 5],
                    "tiledb://TileDB-Inc/c81a36da-1d4b-4119-843e-f3f71b412da4": [3, 4],
                }
            },
        )
