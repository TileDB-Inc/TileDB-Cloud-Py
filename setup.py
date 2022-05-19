# coding: utf-8

"""
    TileDB Cloud Platform Python Client
"""

from setuptools import find_packages  # noqa: H301
from setuptools import setup

# NOTE: we cannot use an __init__.py file in the tiledb/ directory, because it is supplied
#       by core tiledb-py. Therefore, `find_packages` at the root directory does not find
#       any sub-packages. We must explicitly iterate the `tiledb/cloud` subdirectory
# 1) https://packaging.python.org/guides/packaging-namespace-packages/#native-namespace-packages
# 2) https://stackoverflow.com/a/53486554
# Note: we also exclude `namespace_packages` argument, because it causes creation of the
#       '[].nspkg.pth' pointer file, which breaks imports of tiledb.cloud.
# 3) https://stackoverflow.com/a/50301070

PACKAGES = ["tiledb.cloud"]
PACKAGES.extend(
    "tiledb.cloud." + x for x in find_packages("./tiledb/cloud", exclude=("testonly",))
)
VIZ_REQUIRES = ["networkx>=2", "pydot"]
TILEDB_VIZ_REQUIRES = ["tiledb-plot-widget>=0.1.7", *VIZ_REQUIRES]
PLOTLY_VIZ_REQUIRES = ["plotly>=4", *VIZ_REQUIRES]
ALL_REQUIRES = list(set(TILEDB_VIZ_REQUIRES + PLOTLY_VIZ_REQUIRES))

setup(
    name="tiledb-cloud",
    description="TileDB Cloud Platform Python Client",
    author_email="",
    url="https://tiledb.io",
    keywords=["TileDB", "cloud"],
    install_requires=[
        "attrs>=21.4.0",
        "tiledb>=0.5.0",
        "urllib3>=1.26",
        "six>=1.10",
        "certifi",
        "python-dateutil",
        "cloudpickle>=2.0",
        # as of 2021-07-06, the runtime (pinned to 1.1) is incompatible with 1.3
        "pandas<1.3; python_version < '3.10'",
        "pandas>=1.3; python_version >= '3.10'",
        "pyarrow>=3.0.0",
    ],
    extras_require={
        "viz-tiledb": TILEDB_VIZ_REQUIRES,
        "viz-plotly": PLOTLY_VIZ_REQUIRES,
        "all": ALL_REQUIRES,
    },
    packages=PACKAGES,
    include_package_data=True,
    zip_safe=False,  # Force folder install; egg doesn't work for namespace
    long_description="""\
    TileDB Cloud Platform Python API # noqa: E501
    """,
)
