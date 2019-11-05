# coding: utf-8

"""
    TileDB Cloud Platform Python Client
"""

from setuptools import setup, find_packages  # noqa: H301

NAME = "tiledb-cloud"
VERSION = "0.1.2"

# To install the library, run the following
#
# python setup.py install
#
# prerequisite: setuptools
# http://pypi.python.org/pypi/setuptools

REQUIRES = ["tiledb", "urllib3>=1.15", "six>=1.10", "certifi", "python-dateutil", "cloudpickle"]

# NOTE: we cannot use an __init__.py file in the tiledb/ directory, because it is supplied
#       by core tiledb-py. Therefore, `find_packages` at the root directory does not find
#       any sub-packages. We must explicitly iterate the `tiledb/cloud` subdirectory
# 1) https://packaging.python.org/guides/packaging-namespace-packages/#native-namespace-packages
# 2) https://stackoverflow.com/a/53486554
# Note: we also exclude `namespace_packages` argument, because it causes creation of the
#       '[].nspkg.pth' pointer file, which breaks imports of tiledb.cloud.
# 3) https://stackoverflow.com/a/50301070

packages = ['tiledb.cloud'] + ['tiledb.cloud.'+x for x in find_packages("./tiledb/cloud")]

setup(
    name=NAME,
    version=VERSION,
    description="TileDB Cloud Platform Python Client",
    author_email="",
    url="https://tiledb.io",
    keywords=["TileDB", "cloud"],
    install_requires=REQUIRES,
    packages=packages,
    include_package_data=True,
    zip_safe=False, # Force folder install; egg doesn't work for namespace
    long_description="""\
    TileDB Cloud Platform Python API # noqa: E501
    """
)
