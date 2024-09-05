import os
import sys
import uuid

import pytest

import tiledb
import tiledb.cloud
from tiledb.cloud.utilities import get_logger
from tiledb.cloud.utilities import install_wheel
from tiledb.cloud.utilities import upload_wheel
from tiledb.cloud.utilities.wheel import PipInstall

logger = get_logger()

_LOCAL_WHEEL = "tests/utilities/data/fake_unittest_wheel-0.1.0-py3-none-any.whl"
_ARRAY_NAME = os.path.basename(_LOCAL_WHEEL)
_NAMESPACE = tiledb.cloud.client.default_user().username
# Add random suffix to avoid collisions between concurrent tests
_S3_OBJECT_PATH = (
    tiledb.cloud.client.default_user().default_s3_path
    + f"/test-wheel-{str(uuid.uuid4())[-8:]}"
)
_FULL_URI = os.path.join(
    "tiledb://",
    _NAMESPACE,
    _S3_OBJECT_PATH,
    _ARRAY_NAME,
)
_TDB_URI = os.path.join("tiledb://", _NAMESPACE, _ARRAY_NAME)
_CONFIG = tiledb.cloud.Config()


@pytest.fixture
def array_teardown():
    """Handle setup and teardown of arrays.

    Ensures array doesn't exist and deletes if it does.
    Deletes array after tests complete.
    """

    ctx = tiledb.Ctx(_CONFIG)

    try:
        tiledb.Array.delete_array(_FULL_URI, ctx=ctx)
    except tiledb.TileDBError:
        pass

    yield None

    tiledb.Array.delete_array(_FULL_URI, ctx=ctx)


def test_upload_wheel(array_teardown) -> None:
    # first time uploading array
    upload_wheel(
        wheel_path=_LOCAL_WHEEL,
        dest_uri=_FULL_URI,
        overwrite=True,
        config=_CONFIG,
    )

    info = tiledb.cloud.info(os.path.join("tiledb://", _NAMESPACE, _ARRAY_NAME))

    assert info.name == _ARRAY_NAME
    assert info.namespace == _NAMESPACE
    assert info.uri == os.path.join(_S3_OBJECT_PATH, _ARRAY_NAME)

    with pytest.raises(ValueError):
        upload_wheel(
            wheel_path=_LOCAL_WHEEL,
            dest_uri=_FULL_URI,
            overwrite=False,
            config=_CONFIG,
        )

    upload_wheel(
        wheel_path=_LOCAL_WHEEL,
        dest_uri=_FULL_URI,
        overwrite=True,
        config=_CONFIG,
    )


@pytest.fixture
def pip_install_tdb() -> PipInstall:
    """Creates a PipInstall object for tests.

    Uploads a wheel for it to install.
    Deleteds wheel array during teardown.
    """

    # upload a wheel
    upload_wheel(
        wheel_path=_LOCAL_WHEEL,
        dest_uri=_FULL_URI,
        overwrite=True,
        config=_CONFIG,
    )

    pi = PipInstall(
        wheel=_TDB_URI,
        in_venv=True,
    )

    yield pi

    ctx = tiledb.Ctx(_CONFIG)
    tiledb.Array.delete_array(_FULL_URI, ctx=ctx)


def test_pip_install_wheel_ext(pip_install_tdb):
    assert pip_install_tdb.wheel_ext

    pip_install_tdb.wheel = "django"

    assert not pip_install_tdb.wheel_ext


def test_pip_install_rm_from_cache():
    dep = "os"
    observed = PipInstall.rm_from_cache(dep)

    assert len(observed) == 1
    assert dep in observed

    # already removed
    observed2 = PipInstall.rm_from_cache([dep])
    assert not observed2

    dep2 = [dep, "shutil"]
    observed3 = PipInstall.rm_from_cache(dep2)
    assert len(observed3) == 1
    assert dep2[1] in observed3


@pytest.fixture
def pip_install_pypi() -> PipInstall:
    pi = PipInstall(wheel="django", in_venv=True)

    yield pi


def test_pip_install_install(pip_install_pypi):
    # will always run in github actions since django not included
    try:
        import django  # noqa: F401

        logger.info("django already imported, either manually delete or ignore")
    except ModuleNotFoundError:
        pip_install_pypi.install()
        import django  # noqa: F401

        assert "django" in sys.modules
        pip_install_pypi.install(deps_to_refresh="django")
        assert "django" not in sys.modules


def test_install_wheel(pip_install_tdb):
    # install from tiledb cloud array
    assert "fake_unittest_wheel" not in sys.modules

    install_wheel(wheel_uri=_TDB_URI, verbose=True)

    import fake_unittest_wheel  # noqa: F401

    assert "fake_unittest_wheel" in sys.modules
