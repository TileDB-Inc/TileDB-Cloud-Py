import itertools
from functools import partial
from math import ceil
from typing import Any, List, Mapping, Optional, Sequence, TypeVar

from tiledb.cloud.files import utils as file_utils
from tiledb.cloud.utilities import chunk
from tiledb.cloud.utilities import find
from tiledb.cloud.utilities import get_logger_wrapper

DEFAULT_BATCH_SIZE = 100
_T = TypeVar("_T")


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
    logger.info("Searching URI: %s..." % search_uri)

    if include:
        include = partial(file_utils.basename_match, pattern=include)
    if exclude:
        exclude = partial(file_utils.basename_match, pattern=exclude)

    results = list(
        find(
            search_uri,
            include=include,
            exclude=exclude,
            max_count=max_files,
            config=config,
        )
    )

    logger.info("Found %s files." % len(results))
    return results


def chunk_udf(
    items: Sequence[_T],
    batch_size: Optional[int] = None,
    flatten_items: bool = False,
    verbose: bool = False,
) -> List[List[str]]:
    """
    Flatten and break an iterable into batches of a specified size.

    :param items: An iterable to be split into chunks.
    :param batch_size: Resulting chunk size, defaults to None.
    :param flatten_items: If set to True, it will flatten the `items` iterable,
        defaults to False
    :param verbose: Verbose logging, defaults to False
    :return List[List[str]]: A list of chunks as lists.
    """
    logger = get_logger_wrapper(verbose)

    if flatten_items:
        # Flatten the results into a list.
        items = list(itertools.chain.from_iterable(items))
        logger.debug("Flattened list of items to be chunked: %s" % items)

    batch_size = batch_size or DEFAULT_BATCH_SIZE
    batch_size = min(batch_size, len(items))
    num_chunks = ceil(len(items) / batch_size)
    logger.info("Splitting results into %s chunks..." % num_chunks)

    chunked = list(chunk(items, batch_size))
    logger.debug("Chunked results count: %s" % len(chunked))
    logger.debug("First 3 chunks: %s" % chunked[:3])
    return chunked
