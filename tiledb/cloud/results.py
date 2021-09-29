"""Temporary aliases for decoders for UDF environment compatibility."""

from tiledb.cloud._results import decoders

# Compatibility aliases.
# Until a version with decoders.py is deployed to the UDF environment,
# these need to be defined here so that they can be instantiated
# by the name here when pickled and unpickled.
#
# After that, they can be removed, provided this feature has not yet been
# provided in a formal release.


class Decoder(decoders.Decoder):
    pass


class PandasDecoder(decoders.PandasDecoder):
    pass
