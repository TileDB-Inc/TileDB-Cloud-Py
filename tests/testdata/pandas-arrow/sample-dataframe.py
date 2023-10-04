"""The code used to generate the demo dataframes in this directory.

Usage: ``python sample-dataframe.py path/to/output-file.arrow``
"""

import sys

import numpy
import pandas
import pyarrow

from tiledb.cloud._results import codecs


def makedf() -> pandas.DataFrame:
    return pandas.DataFrame(
        {
            "strings": ["a", "b", "c"],
            "floats": [1.0, -0.5, float("nan")],
            "bools": [True, False, None],
            "ints": [0, 1, 2],
            "dates": [
                numpy.datetime64(1695742673, "s"),
                numpy.datetime64(1000000000, "s"),
                numpy.datetime64(1234567890, "s"),
            ],
        }
    )


def main() -> None:
    _, outfile = sys.argv

    df = makedf.makedf()
    arrow_df = pyarrow.Table.from_pandas(df)

    with open(outfile, "wb") as outstream:
        outstream.write(codecs.ArrowDataFrameCodec.encode(arrow_df))


if __name__ == "__main__":
    main()
