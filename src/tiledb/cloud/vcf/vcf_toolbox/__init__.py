import sys

import cloudpickle

from .annotate import annotate
from .transform import df_transform

__all__ = [
    "annotate",
    "df_transform",
]

# Register the module to be pickled by value, so we can use this version of the
# module in a UDF. Otherwise, the module would be pickled by reference, and we
# would use the version of module installed in the UDF docker image.
# This approach enables testing changes to the module before the changes are
# available in the UDF docker image.
cloudpickle.register_pickle_by_value(sys.modules[__name__])
