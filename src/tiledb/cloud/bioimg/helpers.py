import math
import os
from typing import Any, Iterator, Mapping, Sequence, Tuple

import tiledb
#from .types import SupportedExtensions

def get_embeddings_uris(output_file_uri: str) -> Tuple[str, str]:
    destination = os.path.dirname(output_file_uri)
    filename = os.path.basename(output_file_uri).split('.')
    embeddings_flat_uri = os.path.join(destination, f'{filename}_embeddings_flat')
    embeddings_ivf_flat_uri = os.path.join(destination, f'{filename}_embeddings_ivf_flat')
    return embeddings_flat_uri, embeddings_ivf_flat_uri


def serialize_filter(filter):
    if isinstance(filter, tiledb.Filter):
        filter_dict = filter._attrs_()
        filter_dict["_name"] = type(filter).__name__
        return filter_dict
    else:
        raise TypeError


def batch(iterable, chunks):
    # Iterator for providing batches of chunks
    length = len(iterable)
    for ndx in range(0, length, chunks):
        yield iterable[ndx : min(ndx + chunks, length)]


def scale_calc(samples, num_batches):
    """Calculate scaling settings for batch_size and max_workers

    :param source: The source iterable containing files to be ingested/exported
    :param num_batches: The number of batches given by the API
    :return: Tuple batch_size, max_workers
    """
    # If num_batches is default create number of images nodes
    # constraint node max_workers to 20 fully heuristic
    batch_size = 1 if num_batches is None else math.ceil(len(samples) / num_batches)
    max_workers = 20 if num_batches is None else None
    return batch_size, max_workers
