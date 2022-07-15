# TileDB-Cloud-Py

[![Azure Pipelines](https://dev.azure.com/TileDB-Inc/CI/_apis/build/status/TileDB-Inc.TileDB-Cloud-Py?branchName=master)](https://dev.azure.com/TileDB-Inc/CI/_build/latest?definitionId=13&branchName=master)

This repository contains the Python client for the TileDB Cloud Service.

## Quick Links

### Installation

See [Installation Instructions](https://docs.tiledb.com/cloud/client-api/installation)

### Quickstart

See [Quickstart](https://docs.tiledb.com/cloud/quickstart) section of the docs.

### Testing

* Selection:
  * All tests: `pytest`
  * All tests with verbosity: `pytest -vs`
  * Tests with `taskgraphs` in their names: `pytest -vsk taskgraphs`
* Credentials:
  * These tests run on TileDB Cloud using your current environment variable `TILEDB_REST_TOKEN` -- you will need a valid API token for the tests to pass
  * For continuous integration, the token is configured for the `unittest` user and all tests should pass
  * For interactive use, if your `TILEDB_REST_TOKEN` points to your own account, most tests will run, except for those that explicit check against contents of the `unittest` account which are skipped
