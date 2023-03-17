"""Minimal replacement for ``pandas._libs.arrays``."""

from pandas.core.arrays import _mixins

NDArrayBacked = _mixins.NDArrayBackedExtensionArray


# Based on generated Cython code.
# https://github.com/cython/cython/blob/0.29.33/Cython/Compiler/ParseTreeTransforms.py#L1713-L1722
def __pyx_unpickle_NDArrayBacked(typ, checksum, state):
    if checksum not in (0xD555CB8, 0x4F1061F, 0xB63B53E):
        raise ValueError(
            f"unknown NDArrayBacked pickle checksum {checksum:08x};"
            " this version of TileDB Cloud is not compatible"
            " with this Pandas pickle data"
        )
    result = NDArrayBacked.__new__(typ)  # type: ignore[var-annotated]
    if state is not None:
        # This is equivalent to the Cython code that was originally generated.
        result.__setstate__(state)
    return result
