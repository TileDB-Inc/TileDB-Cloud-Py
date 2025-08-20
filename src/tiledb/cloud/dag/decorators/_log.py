from tiledb.cloud.utilities.logging import get_logger

logger = get_logger()


def log_submission(
    namespace: str,
    server_graph_uuid: str,
    log_url: str = "https://cloud.tiledb.com/activity/taskgraphs/{}/{}",
) -> str:
    """Log submission of task graph."""

    task_uri = log_url.format(namespace, server_graph_uuid)
    logger.info(f"Task graph submitted - {task_uri}")

    return task_uri
