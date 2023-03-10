def patch_pandas() -> None:
    """Makes Pandas v1.2.x able to unpickle Pandas v1.3+ DataFrames."""
    from pandas.core.internals import blocks

    if hasattr(blocks, "new_block"):
        # We already support unpickling v1.3+ DataFrames.
        return

    # Import these extremely lazily so we don't reach into Pandas internals
    # unless we ABSOLUTELY need to.
    import pandas._libs.internals as pdinternals
    from pandas.core.dtypes import dtypes

    # The following code is taken from Pandas v1.5.3 under the BSD license:
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
    # https://github.com/pandas-dev/pandas/blob/v1.5.3/pandas/core/internals/blocks.py#L2172
    def _new_block(values, placement, *, ndim: int) -> blocks.Block:
        # caller is responsible for ensuring values is NOT a PandasArray

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
    def _check_ndim(values, placement: pdinternals.BlockPlacement, ndim: int) -> None:
        if values.ndim > ndim:
            # Check for both np.ndarray and ExtensionArray
            raise ValueError(
                "Wrong number of dimensions. "
                f"values.ndim > ndim [{values.ndim} > {ndim}]"
            )

        elif not _is_1d_only_ea_dtype(values.dtype):
            # TODO(EA2D): special case not needed with 2D EAs
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
            # TODO(EA2D): special case unnecessary with 2D EAs
            raise ValueError("need to split")

    # https://github.com/pandas-dev/pandas/blob/v1.5.3/pandas/core/dtypes/common.py#L1420
    def _is_1d_only_ea_dtype(dtype) -> bool:
        # Note: if other EA dtypes are ever held in HybridBlock, exclude those
        #  here too.
        # NB: need to check DatetimeTZDtype and not is_datetime64tz_dtype
        #  to exclude ArrowTimestampUSDtype
        return isinstance(dtype, dtypes.ExtensionDtype) and not isinstance(
            dtype, (dtypes.DatetimeTZDtype, dtypes.PeriodDtype)
        )

    # https://github.com/pandas-dev/pandas/blob/v1.5.3/pandas/_libs/internals.pyx#L570
    def _new_block_trampoline(values, placement, ndim) -> blocks.Block:
        return _new_block(values, placement, ndim=ndim)

    blocks.new_block = _new_block
    pdinternals._unpickle_block = _new_block_trampoline
