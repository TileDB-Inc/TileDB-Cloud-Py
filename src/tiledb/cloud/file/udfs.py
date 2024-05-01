from functools import partial
from math import ceil
from typing import Any, List, Mapping, Optional, Sequence, TypeVar

from tiledb.cloud.file import utils as file_utils
from tiledb.cloud.utilities import chunk
from tiledb.cloud.utilities import find
from tiledb.cloud.utilities import get_logger_wrapper

DEFAULT_BATCH_SIZE = 100
T = TypeVar("T")


def find_uris_udf(
    search_uri: str,
    *,
    config: Optional[Mapping[str, Any]] = None,
    include: Optional[str] = None,
    exclude: Optional[str] = None,
    max_files: Optional[int] = None,
    verbose: bool = False,
) -> Sequence[str]:
    """
    Find URIs matching a pattern in the `search_uri` path.

    `include` and `exclude` patterns are Unix shell style (see fnmatch module).

    :param search_uri: URI to search for files
    :param config: config dictionary, defaults to None
    :param include: include pattern used in the search, defaults to None
    :param exclude: exclude pattern applied to the search results, defaults to None
    :param max_files: maximum number of URIs returned, defaults to None
    :param verbose: verbose logging, defaults to False
    :return: list of URIs
    """
    logger = get_logger_wrapper(verbose)

    search_uri = search_uri.rstrip("/") + "/"
    logger.info(f"Searching URI: {search_uri}...")

    if include:
        include = partial(file_utils.basename_match, pattern=include)
    if exclude:
        exclude = partial(file_utils.basename_match, pattern=exclude)

    results = [
        *find(
            search_uri,
            include=include,
            exclude=exclude,
            max_count=max_files,
            config=config,
        )
    ]

    logger.info(f"Found {len(results)} files.")
    return results


def chunk_udf(
    items: Sequence[T],
    batch_size: Optional[int] = None,
    flatten_items: bool = False,
    verbose: bool = False,
) -> List[List[str]]:
    """
    Flatten and break a list of udf results into batches of a specified size.

    :param udf_results: An iterable of iterables containing UDF results.
    :param batch_size: Resulting chunk size, defaults to None.
    :return List[List[str]]: A list of chunks as lists.
    """
    logger = get_logger_wrapper(verbose)

    if flatten_items:
        # Flatten the results into a list.
        items = [elem for item in items for elem in item]
        logger.debug(f"Flattened list of items to be chunked: {items}")

    batch_size = batch_size or DEFAULT_BATCH_SIZE
    batch_size = min(batch_size, len(items))
    num_chunks = ceil(len(items) / batch_size)
    logger.info(f"Splitting results into {num_chunks} chunks...")

    chunked = [*chunk(items, batch_size)]
    logger.debug(f"Chunked results count: {len(chunked)}")
    logger.debug(f"First 3 chunks: {chunked[:3]}")
    return chunked
