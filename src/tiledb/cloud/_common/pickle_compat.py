import importlib
import sys

import numpy
import packaging.version as pkgver
import pandas


def patch_pandas() -> None:
    """Make older Pandas versions able to unpickle new Pandas dataframes."""

    pandas_ver = pkgver.parse(pandas.__version__)
    if pkgver.parse("1.5") <= pandas_ver:
        # v1.5 is the newest version as of this writing.
        return

    # Import everything else EXTREMELY lazily so we don't mess with Pandas
    # internals any more than we absolutely need to.
    import pandas._libs.internals as pdinternals
    from pandas.core.internals import blocks

    # Functions below are adapted from Pandas code and are used under
    # the BSD license:
    #
    # BSD 3-Clause License
    #
    # Copyright (c) 2008-2011, AQR Capital Management, LLC, Lambda Foundry, Inc.
    # and PyData Development Team
    # All rights reserved.
    #
    # Copyright (c) 2011-2022, Open source contributors.
    #
    # Redistribution and use in source and binary forms, with or without
    # modification, are permitted provided that the following conditions
    # are met:
    #
    # * Redistributions of source code must retain the above copyright notice,
    #   this list of conditions and the following disclaimer.
    #
    # * Redistributions in binary form must reproduce the above copyright
    #   notice, this list of conditions and the following disclaimer in the
    #   documentation and/or other materials provided with the distribution.
    #
    # * Neither the name of the copyright holder nor the names of its
    #   contributors may be used to endorse or promote products derived from
    #   this software without specific prior written permission.
    #
    # THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
    # "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
    # LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS
    # FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE
    # COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT,
    # INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING,
    # BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
    # LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED
    # AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
    # OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF
    # THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY
    # OF SUCH DAMAGE.

    if not hasattr(blocks, "new_block"):
        from pandas.core.dtypes import dtypes

        # https://github.com/pandas-dev/pandas/blob/v1.5.3/pandas/core/internals/blocks.py#L2172
        def _patch_new_block(values, placement, *, ndim: int) -> blocks.Block:
            if not isinstance(placement, pdinternals.BlockPlacement):
                placement = pdinternals.BlockPlacement(placement)

            _check_ndim(values, placement, ndim)

            # don't want to pass `values.dtype` here.
            klass = blocks.get_block_type(values)

            # OMITTED:
            #     we don't attempt to coerce values here because all our inputs
            #     come from Pandas serialization, so we assume that they're valid.
            # values = maybe_coerce_values(values)

            return klass(values, ndim=ndim, placement=placement)

        # https://github.com/pandas-dev/pandas/blob/v1.5.3/pandas/core/internals/blocks.py#L2186
        def _check_ndim(
            values, placement: pdinternals.BlockPlacement, ndim: int
        ) -> None:
            if values.ndim > ndim:
                raise ValueError(
                    "Wrong number of dimensions. "
                    f"values.ndim > ndim [{values.ndim} > {ndim}]"
                )

            elif not _is_1d_only_ea_dtype(values.dtype):
                if values.ndim != ndim:
                    raise ValueError(
                        "Wrong number of dimensions. "
                        f"values.ndim != ndim [{values.ndim} != {ndim}]"
                    )
                if len(placement) != len(values):
                    raise ValueError(
                        f"Wrong number of items passed {len(values)}, "
                        f"placement implies {len(placement)}"
                    )
            elif ndim == 2 and len(placement) != 1:
                raise ValueError("need to split")

        # https://github.com/pandas-dev/pandas/blob/v1.5.3/pandas/core/dtypes/common.py#L1420
        def _is_1d_only_ea_dtype(dtype) -> bool:
            return isinstance(dtype, dtypes.ExtensionDtype) and not isinstance(
                dtype, (dtypes.DatetimeTZDtype, dtypes.PeriodDtype)
            )

        blocks.new_block = _patch_new_block

    if not hasattr(pdinternals, "_unpickle_block"):
        # https://github.com/pandas-dev/pandas/blob/v1.5.3/pandas/_libs/internals.pyx#L570
        def _new_block_trampoline(values, placement, ndim) -> blocks.Block:
            return blocks.new_block(values, placement, ndim=ndim)

        pdinternals._unpickle_block = _new_block_trampoline

    # pandas._libs.arrays is used by certain pickles that use storage
    # backed by NumPy NDArrays.
    try:
        import pandas._libs.arrays as _unused_pla  # noqa: F401
    except ImportError:
        import pandas._libs as pdlibs

        from . import _array_backed

        pdlibs.arrays = _array_backed
        sys.modules["pandas._libs.arrays"] = _array_backed
        importlib.invalidate_caches()

        if not hasattr(_array_backed.NDArrayBacked, "__setstate__"):
            # https://github.com/pandas-dev/pandas/blob/v1.5.3/pandas/_libs/arrays.pyx#L81
            def _patch_setstate(self, state):
                if isinstance(state, dict):
                    if "_data" in state:
                        data = state.pop("_data")
                    elif "_ndarray" in state:
                        data = state.pop("_ndarray")
                    else:
                        raise ValueError  # pragma: no cover
                    self._data = data  # CHANGED: This is now `_data`.
                    self._dtype = state.pop("_dtype")

                    for key, val in state.items():
                        setattr(self, key, val)
                elif isinstance(state, tuple):
                    if len(state) != 3:
                        if len(state) == 1 and isinstance(state[0], dict):
                            self.__setstate__(state[0])
                            return
                        raise NotImplementedError(state)  # pragma: no cover

                    data, dtype = state[:2]
                    if isinstance(dtype, numpy.ndarray):
                        dtype, data = data, dtype
                    self._data = data  # CHANGED: This is now _data.
                    self._dtype = dtype

                    if isinstance(state[2], dict):
                        for key, val in state[2].items():
                            setattr(self, key, val)
                    else:
                        raise NotImplementedError(state)  # pragma: no cover
                else:
                    raise NotImplementedError(state)  # pragma: no cover

            _array_backed.NDArrayBacked.__setstate__ = _patch_setstate
