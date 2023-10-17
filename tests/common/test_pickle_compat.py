import pathlib
import pickle
import sys
from typing import Any, Tuple

import numpy as np
import packaging.version as pkgver
import pandas as pd
import pytest

SIMPLE_DF = pd.DataFrame(
    [
        [1, 1.1, "one"],
        [2, 2.2, "two"],
    ],
    columns=("nt", "flt", "strng"),
)

NDARRAY_BACKED_DF = pd.DataFrame(
    {
        "timestamp": np.array(
            (27984459, 27996857, 27988084, 27983388, 27993584), dtype="datetime64[m]"
        ),
        "x": (10.5, 15.7, 19.0, 10.5, 16.7),
        "y": (3.94, 3.44, 3.75, 3.21, 3.91),
        "z": (9, -5, 4, 8, 7),
    }
)
# Additional verification that `xarrays` will work based on customer need.
XARRAY = NDARRAY_BACKED_DF.set_index(["x", "y", "timestamp"]).to_xarray()

RESULTS = {
    "simple_df": SIMPLE_DF,
    "ndarray_backed_df": NDARRAY_BACKED_DF,
    "xarray": XARRAY,
}

PICKLE_DIR = pathlib.Path(__file__).parent / "testdata" / "pickles"


@pytest.fixture(scope="module", autouse=True)
def import_tiledb_cloud():
    # We import tiledb.cloud but don't use it so that we can be sure that
    # Pandas is immediately patched upon importing `tiledb.cloud`.
    import tiledb.cloud  # noqa: F401


@pytest.mark.skipif(
    pkgver.Version("2") <= pkgver.Version(pd.__version__),
    reason="Pandas 2 is an unresolvable breaking change",
)
@pytest.mark.parametrize("pd_ver", ["1.2.4", "1.5.3"])
@pytest.mark.parametrize("name_want", RESULTS.items(), ids=lambda itm: itm[0])
def test_pandas_compat(pd_ver: str, name_want: Tuple[str, Any]) -> None:
    name, want = name_want
    pkl_file = PICKLE_DIR / "pandas" / f"{name}-pd{pd_ver}.pickle"
    pkl_bytes = pkl_file.read_bytes()
    got = pickle.loads(pkl_bytes)
    assert want.equals(got)


# These are the versions of cloudpickle that introduce serialization changes.
@pytest.mark.parametrize("cp_ver", ["1.4.1", "1.5.0", "2.1.0"])
def test_cloudpickle_compat(cp_ver: str) -> None:
    py_ver = ".".join(str(v) for v in sys.version_info[:2])
    pkl_file = PICKLE_DIR / "functions" / f"func-py{py_ver}-cloudpickle{cp_ver}.pickle"
    pkl_bytes = pkl_file.read_bytes()
    got_func = pickle.loads(pkl_bytes)
    val = got_func()
    assert val == "the date is 2023-05-05 07:00"
