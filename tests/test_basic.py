import tiledb, tiledb.cloud
import os

tiledb.cloud.login(token=os.environ["TILEDB_CLOUD_HELPER_VAR"])


def test_quickstart():
    with tiledb.open(
        "tiledb://TileDB-Inc/quickstart_dense", ctx=tiledb.cloud.Ctx()
    ) as A:
        print("quickstart_dense:")
        print(A[:])

    with tiledb.open(
        "tiledb://TileDB-Inc/quickstart_sparse", ctx=tiledb.cloud.Ctx()
    ) as A:
        print("quickstart_sparse:")
        print(A[:])
