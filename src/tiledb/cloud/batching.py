import math

import tiledb


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


def serialize_filter(filter):
    if isinstance(filter, tiledb.Filter):
        filter_dict = filter._attrs_()
        filter_dict["_name"] = type(filter).__name__
        return filter_dict
    else:
        raise TypeError
