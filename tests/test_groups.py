import random

import numpy as np
import pandas as pd

import tiledb
import tiledb.cloud
import tiledb.cloud.array
import tiledb.cloud.group


def make_name(base):
    lowers = "abcdefghijklmnopqrstuvwxyz"
    length = 12
    word = ""
    for j in range(0, length):
        word += random.choice(lowers)
    return base + word


def make_array(name):
    x = [1, 2, 3, 4, 5]
    y = [e**2 for e in x]
    dataframe = pd.DataFrame.from_dict(
        {
            "x": np.asarray(x),
            "y": np.asarray(y),
        },
    )
    namespace = tiledb.cloud.user_profile().username
    s3_temp = "s3://tiledb-johnkerl/scratch/try101"
    pre_creation_uri = f"tiledb://{namespace}/{s3_temp}/{name}"
    post_creation_uri = f"tiledb://{namespace}/{name}"
    tiledb.from_pandas(
        uri=pre_creation_uri,
        dataframe=dataframe,
        name=name,
    )
    print("made array", post_creation_uri)
    return post_creation_uri


def unmake_array(uri):
    tiledb.cloud.array.delete_array(uri)


def make_group(name):
    namespace = tiledb.cloud.user_profile().username
    s3_temp = "s3://tiledb-johnkerl/scratch/try101"
    pre_creation_uri = f"tiledb://{namespace}/{s3_temp}/{name}"
    post_creation_uri = f"tiledb://{namespace}/{name}"
    tiledb.group_create(uri=pre_creation_uri)
    print("made group", post_creation_uri)
    return post_creation_uri


def make_nested_group():
    g1_name = make_name("ut-g1-")
    g2_name = make_name("ut-g2-")
    a1_name = make_name("ut-a1-")
    a2_name = make_name("ut-a2-")
    a3_name = make_name("ut-a3-")

    a2_uri = make_array(a2_name)
    a3_uri = make_array(a3_name)
    g2_uri = make_group(g2_name)
    a1_uri = make_array(a1_name)
    g1_uri = make_group(g1_name)

    with tiledb.Group(g2_uri, mode="w") as G2:
        G2.add(uri=a2_uri, relative=False, name=a2_name)
        G2.add(uri=a3_uri, relative=False, name=a3_name)
    with tiledb.Group(g1_uri, mode="w") as G1:
        G1.add(uri=g2_uri, relative=False, name=g2_name)
        G1.add(uri=a1_uri, relative=False, name=a1_name)

    return g1_uri


def unmake_nested_group(uri):
    tiledb.cloud.delete_group_recursively(uri)


# test get_group
# test _get_group_element_tiledb_uris
# test delete_group_recursively

# if __name__ == "__main__":
# uri = make_array('testing-testing-123')
# unmake_array(uri)

# use get_group to enumerate
# use vfs to check s3 existence

# uri = make_nested_group()
# info = tiledb.cloud.group.get_group(uri)
# print("PRE INFO")
# print(info)
# print("POST INFO")
# unmake_nested_group("tiledb://johnkerl-tiledb/group--bjkcyetvajmt")

# use get_group results to check
# use vfs to check s3 non-existence
