#!/usr/bin/env python

import pathlib
import pickle

import pandas as pd

from . import test_pickle_compat

PICKLEABLES = test_pickle_compat.RESULTS


def main() -> None:
    import argparse

    p = argparse.ArgumentParser()
    p.add_argument("out-dir", required=True)
    args = p.parse_args()

    out_dir_path = pathlib.Path(args.out_dir)

    for name in PICKLEABLES:
        out_file = out_dir_path / f"{name}-pd{pd.__version__}.pickle"
        with out_file.open("wb") as out_stream:
            pickle.dump(PICKLEABLES[name], out_stream)


if __name__ == "__main__":
    main()
