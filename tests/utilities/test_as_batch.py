"""Tests of as_batch() and of the _resources parameter tunnel."""

import unittest
import unittest.mock

import tiledb.cloud.utilities._common
from tiledb.cloud.utilities._common import as_batch


@unittest.mock.patch.object(tiledb.cloud.utilities._common.dag, "DAG")
def test_propagate_resources(mock_dag):
    """Assert that as_batch propagates resource parameters."""

    def submit(func, *args, **kwargs):
        """Roughly mimic DAG.submit()."""
        _ = kwargs.pop("resource_class", None)
        _ = kwargs.pop("resources", None)
        func(*args, **kwargs)

    mock_dag.configure_mock(**{"return_value.submit.side_effect": submit})

    def func(*args, **kwargs):
        """Demonstrate that the wrapped function receives resources."""
        assert "_resources" in kwargs
        assert kwargs["_resources"]["resource_class"] == "foo"
        assert kwargs["_resources"]["resources"] == {"cpu": "8", "memory": "32Gi"}

    as_batch(func)(resource_class="foo", resources={"cpu": "8", "memory": "32Gi"})
