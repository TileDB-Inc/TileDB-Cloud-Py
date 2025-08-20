from typing import Any, Mapping, Sequence, Union

from tiledb.cloud.dag import DAG
from tiledb.cloud.utilities.logging import get_logger

logger = get_logger()


def log_tg_submission(
    namespace: str,
    server_graph_uuid: str,
    log_url: str = "https://cloud.tiledb.com/activity/taskgraphs/{}/{}",
) -> str:
    """Log submission of task graph."""

    task_uri = log_url.format(namespace, server_graph_uuid)
    logger.info(f"Task graph submitted - {task_uri}")

    return task_uri


def log_node_submission(
    name: str,
    dag: DAG,
    args: Sequence[Any],
    kwargs: Mapping[str, Any],
    resources: Union[str, Mapping[str, str]],
) -> None:
    """Log submission of node."""

    logger.info(f"> Submit UDF {name} to {dag}")
    logger.info(f"|---args = {args}")
    logger.info(f"|---kwargs = {kwargs}")
    logger.info(f"|---resources = {resources}")
