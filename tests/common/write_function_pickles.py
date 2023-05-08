#!/usr/bin/env python

import datetime
import pathlib
import sys
from typing import Callable

import cloudpickle


def outer() -> Callable[[], Callable[[], str]]:
    the_date = datetime.datetime(2023, 5, 5, 7, tzinfo=datetime.timezone.utc)

    def inner() -> str:
        import builtins

        return builtins.str.format("the date is {:%Y-%m-%d %H:%M}", the_date)

    return inner


PY_VER = ".".join(str(v) for v in sys.version_info[:2])
CP_VER = cloudpickle.__version__


def main() -> None:
    import argparse

    p = argparse.ArgumentParser()
    p.add_argument("out_dir")
    args = p.parse_args()

    out_dir_path = pathlib.Path(args.out_dir)

    out_file = out_dir_path / f"func-py{PY_VER}-cloudpickle{CP_VER}.pickle"
    with out_file.open("wb") as out_stream:
        cloudpickle.dump(outer(), out_stream)


if __name__ == "__main__":
    main()
