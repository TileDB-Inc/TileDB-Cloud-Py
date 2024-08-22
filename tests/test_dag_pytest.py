"""Pytest-based tests for tiledb.cloud.dag.dag"""

from unittest.mock import MagicMock
from unittest.mock import patch
from webbrowser import Error

from attrs import define

import tiledb.cloud
from tiledb.cloud.dag.dag import exec_batch_udf
from tiledb.cloud.dag.mode import Mode

_TASK_NAME = "unittest-test-dag-exec-batch-udf"
_NAMESPACE = tiledb.cloud.client.default_user().username


@define
class ExecutableLoader:
    arg: str = "arg1"
    registered_udf: str = "TileDB-Inc/ls_uri"

    def in_memory(self, arg: str):
        return arg

    @property
    def registered(self):
        return self.registered_udf

    def all_exec(self):
        return (
            self.in_memory,
            self.registered,
        )


@patch("tiledb.cloud.dag.dag.webbrowser.open_new_tab")
@patch("tiledb.cloud.dag.dag.DAG")
def test_exec_batch_udf_mock(mock_dag: MagicMock, mock_open_new_tab: MagicMock) -> None:
    """Test procedure of exec_batch_udf.

    This test is concerned only if proper logic is engaged based on args and exceptions.

    Additionally by passing both an in-memory callable and a str referencing
    a registered UDF, checks that the name of the submitted node is set properly
    and no AttributeError thrown.
    """

    mock_dag_inst = mock_dag.return_value

    loader = ExecutableLoader()

    expected_submit_call_count = 0
    for callable_to_test in loader.all_exec():
        expected_submit_call_count += 1

        graph = exec_batch_udf(
            callable_to_test,
            loader.arg,
            compute=False,
        )

        assert mock_dag_inst.submit.call_count == expected_submit_call_count
        assert mock_dag_inst.compute.call_count == 0
        assert isinstance(graph, MagicMock)

    # checking logic associated with open_browser == True
    # ensure 'except' block hits when trying to open webbrowser
    mock_open_new_tab.side_effect = Error()

    graph = exec_batch_udf(
        loader.in_memory,
        loader.arg,
        compute=True,
        open_browser=True,
    )

    assert mock_dag_inst.submit.call_count == expected_submit_call_count + 1
    assert mock_dag_inst.compute.call_count == 1
    assert mock_open_new_tab.called  # test webbrowser attempted to open


def test_exec_batch_udf() -> None:
    """Test actual loading of DAG.

    Here, concerned with DAG is instantiated appropriately as specified
    by exec_batch_udf.

    Previous unit test for exec_batch_udf already tested compute method is called
    when the 'compute' arg is True. So not actually executing batch UDF, as
    DAG.compute is tested elsewhere, outside of scope of these tests.

    Does not test whether the registered UDF actually exists, just that
    a str passed is acceptable. It is on the user to ensure registered
    UDF exists.
    """

    loader = ExecutableLoader()

    # test multiple retry limit settings
    for retry_count, callable_to_test in enumerate(loader.all_exec()):
        graph = exec_batch_udf(
            callable_to_test,
            loader.arg,
            name=_TASK_NAME,
            namespace=_NAMESPACE,
            retry_limit=retry_count,
            compute=False,
        )

        assert graph.name == f"batch->{_TASK_NAME}"
        assert graph.namespace == _NAMESPACE
        assert graph.mode == Mode.BATCH
        assert graph.retry_strategy.retry_policy.lower() == "always"
        assert graph.retry_strategy.limit == retry_count
        assert len(graph.nodes) == 1
        assert graph.status.name.lower() == "not_started"
