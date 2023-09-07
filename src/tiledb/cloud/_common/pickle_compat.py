"""A series of hacks to allow us to read ordinarily-incompatible pickles.

A complex pickle stream consists of essentially constructing a bunch of values
and then passing those values into already-installed library functions.
In many cases, the only reason that a pickle cannot be loaded is because the
library function that the pickle stream refers to is not present;
monkey-patching the function in may allow the pickle to be read.

This monkey-patches a few libraries to enable read-compatibility of pickles.
Changing the pickle-writing process would be much more difficult.
"""

import importlib
import sys
import types

import cloudpickle.cloudpickle as cpcp
import importlib_metadata
import numpy
import packaging.version as pkgver


def patch_cloudpickle() -> None:
    """Make older cloudpickle versions able to unpickle new function pickles."""

    # Functions below are adapted from cloudpickle v2.2.1
    # under the BSD license:
    #
    # Copyright (c) 2012, Regents of the University of California.
    # Copyright (c) 2009 PiCloud, Inc.
    #     <https://web.archive.org/web/20140626004012/http://www.picloud.com/>.
    # All rights reserved.
    #
    # Redistribution and use in source and binary forms, with or without
    # modification, are permitted provided that the following conditions
    # are met:
    #     * Redistributions of source code must retain the above copyright
    #       notice, this list of conditions and the following disclaimer.
    #     * Redistributions in binary form must reproduce the above copyright
    #       notice, this list of conditions and the following disclaimer in the
    #       documentation and/or other materials provided with the distribution.
    #     * Neither the name of the University of California, Berkeley nor the
    #       names of its contributors may be used to endorse or promote
    #       products derived from this software without specific prior written
    #       permission.
    #
    # THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
    # "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
    # LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
    # A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT
    # HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
    # SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED
    # TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR
    # PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF
    # LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING
    # NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
    # SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

    try:
        empty_cell_value = cpcp._empty_cell_value
    except AttributeError:
        # https://github.com/cloudpipe/cloudpickle/blob/v2.2.1/cloudpickle/cloudpickle.py#L692-L698
        class _empty_cell_value:
            """sentinel for empty closures"""

            @classmethod
            def __reduce__(cls):
                return cls.__name__

        _empty_cell_value.__module__ = cpcp.__name__
        empty_cell_value = _empty_cell_value()
        cpcp._empty_cell_value = empty_cell_value

    try:
        make_empty_cell = cpcp._make_empty_cell
    except AttributeError:
        # https://github.com/cloudpipe/cloudpickle/blob/v2.2.1/cloudpickle/cloudpickle.py#L772-L778
        def make_empty_cell():
            if False:
                # trick the compiler into creating an empty cell in our lambda
                cell = None
                raise AssertionError("this route should not be executed")

            return (lambda: cell).__closure__[0]

    if not hasattr(types, "CellType"):
        types.CellType = type(make_empty_cell())

    if not hasattr(cpcp, "_make_cell"):
        try:
            cell_set = cpcp.cell_set
        except AttributeError:
            #
            def cell_set(cell, value):
                # We only support 3.7+.
                cell.cell_contents = value

            cpcp.cell_set = cell_set

        # https://github.com/cloudpipe/cloudpickle/blob/v2.2.1/cloudpickle/cloudpickle.py#L392-L450
        def _make_cell(value=empty_cell_value):
            cell = make_empty_cell()
            if value is not empty_cell_value:
                cell_set(cell, value)
            return cell

        cpcp._make_cell = _make_cell

    if not hasattr(cpcp, "_make_function"):

        def _make_function(code, globals, name, argdefs, closure):
            # Setting __builtins__ in globals is needed for nogil CPython.
            globals["__builtins__"] = __builtins__
            return types.FunctionType(code, globals, name, argdefs, closure)

        cpcp._make_function = _make_function


def patch_pandas() -> None:
    """Make older Pandas versions able to unpickle new Pandas dataframes."""

    try:
        pandas_ver_str = importlib_metadata.version("pandas")
    except Exception:
        # Not installed via the usual means; just import it and see
        # what version we have.
        import pandas

        pandas_ver_str = pandas.__version__

    if pkgver.parse("1.5") <= pkgver.parse(pandas_ver_str):
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
