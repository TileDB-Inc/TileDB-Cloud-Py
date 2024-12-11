# TileDB-Cloud-Py

This repository contains the Python client for the TileDB Cloud Service.

## Quick Links

### Installation

See [Installation Instructions](https://docs.tiledb.com/cloud/client-api/installation)

### Quickstart

See [Quickstart](https://docs.tiledb.com/cloud/quickstart) section of the docs.

### API Documentation

See https://tiledb-inc.github.io/TileDB-Cloud-Py/

#### Contribute to documentation

Documentation uses [Quarto](https://quarto.org/) style documentation.

- Install [Quarto for your OS](https://quarto.org/docs/get-started/)
- Install documentation dependencies: `pip install .[docs]`
- Update the [docs/\_quarto.yaml](docs/_quarto.yaml) file accordingly ([read the quartodoc documentation on how to do that](https://quarto.org/docs/get-started/))
- Build the docs: `quartodoc build --config docs/_quarto.yaml`
- Preview the generated docs: `quarto preview docs/`
- Create a relevant PR

### Testing

- Selection:
  - All tests: `pytest`
  - All tests with verbosity: `pytest -vs`
  - Tests with `taskgraphs` in their names: `pytest -vsk taskgraphs`
- Credentials:
  - These tests run on TileDB Cloud using your current environment variable `TILEDB_REST_TOKEN` -- you will need a valid API token for the tests to pass
  - For continuous integration, the token is configured for the `unittest` user and all tests should pass
  - For interactive use, if your `TILEDB_REST_TOKEN` points to your own account, most tests will run, except for those that explicitly check against contents of the `unittest` account which are skipped

### Ingestion testing

This package contains modules and functions that will be run in the TileDB Cloud as UDFs. Local ingestor changes can be tested in the cloud by using a feature of [cloudpickle](https://github.com/cloudpipe/cloudpickle?tab=readme-ov-file#overriding-pickles-serialization-mechanism-for-importable-constructs). Below is a runnable example. `TILEDB_NAMESPACE` is your TileDB namespace ("TileDB-Inc", for example). `TILEDB_ACCESS_CREDENTIAL_NAME` is the name of the stored credentials for accessing `AWS_BUCKET`. `IMAGE_FILE_KEY` is the key for an object in that bucket and `OUTPUT_GROUP_KEY` is the key to be used for the group that the `ingest()` UDF will create in `AWS_BUCKET`.

```python
from tiledb.cloud._vendor import cloudpickle

import tiledb.cloud.bioimg

cloudpickle.register_pickle_by_value(tiledb.cloud.bioimg)

tiledb.cloud.bioimg.ingest(
    source="s3://AWS_BUCKET/IMAGE_FILE_KEY",
    output="s3://AWS_BUCKET/OUTPUT_GROUP_KEY",
    config=None,
    namespace="TILEDB_NAMESPACE",
    acn="TILEDB_ACCESS_CREDENTIAL_NAME",
    ingest_resources={"cpu": "8", "memory": "32Gi"},
)
```

In this case `tiledb.cloud.bioimg.ingest()` uses cloudpickle to send a local function to TileDB Cloud, and `tdbcp.register_pickle_by_value(tiledb.cloud.bioimg)` directs cloudpickle to bring the currently imported `tiledb.cloud.bioimg` module along with the function. Your local version of the module will be used instead of the version currently deployed in TileDB Cloud.

Note: your local changes to the Cloud-Py package will need to be installed in order for cloudpickle to serialize them, as cloudpickle needs to find them at runtime.

### Releasing

Releasing is entirely automated. Releases made on GitHub using tags that start with "v", like "v0.12.28", trigger sdist and wheel builds and upload of those distributions to the Python Package Index.
