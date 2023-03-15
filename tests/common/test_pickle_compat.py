import base64
import pickle
import unittest

import pandas as pd

# We import tiledb.cloud but don't use it so that we can be sure that
# Pandas is immediately patched upon importing `tiledb.cloud`.
import tiledb.cloud  # noqa: F401

_WANT_DF = pd.DataFrame(
    [
        [1, 1.1, "one"],
        [2, 2.2, "two"],
    ],
    columns=("nt", "flt", "strng"),
)


class PickleCompatTest(unittest.TestCase):
    def test_old_pickle(self):
        # Produced by pickling _WANT_DF with Pandas 1.2.5.
        old_pickle = base64.b64decode(
            """
            gASV9gMAAAAAAACMEXBhbmRhcy5jb3JlLmZyYW1llIwJRGF0YUZyYW1llJOUKYGUfZQo
            jARfbWdylIwecGFuZGFzLmNvcmUuaW50ZXJuYWxzLm1hbmFnZXJzlIwMQmxvY2tNYW5h
            Z2VylJOUKYGUKF2UKIwYcGFuZGFzLmNvcmUuaW5kZXhlcy5iYXNllIwKX25ld19JbmRl
            eJSTlGgLjAVJbmRleJSTlH2UKIwEZGF0YZSMFW51bXB5LmNvcmUubXVsdGlhcnJheZSM
            DF9yZWNvbnN0cnVjdJSTlIwFbnVtcHmUjAduZGFycmF5lJOUSwCFlEMBYpSHlFKUKEsB
            SwOFlGgVjAVkdHlwZZSTlIwCTziUiYiHlFKUKEsDjAF8lE5OTkr/////Sv////9LP3SU
            YoldlCiMAm50lIwDZmx0lIwFc3RybmeUZXSUYowEbmFtZZROdYaUUpRoDYwZcGFuZGFz
            LmNvcmUuaW5kZXhlcy5yYW5nZZSMClJhbmdlSW5kZXiUk5R9lChoKU6MBXN0YXJ0lEsA
            jARzdG9wlEsCjARzdGVwlEsBdYaUUpRlXZQoaBRoF0sAhZRoGYeUUpQoSwFLAUsChpRo
            HowCZjiUiYiHlFKUKEsDjAE8lE5OTkr/////Sv////9LAHSUYolDEJqZmZmZmfE/mpmZ
            mZmZAUCUdJRiaBRoF0sAhZRoGYeUUpQoSwFLAUsChpRoHowCaTiUiYiHlFKUKEsDaD1O
            Tk5K/////0r/////SwB0lGKJQxABAAAAAAAAAAIAAAAAAAAAlHSUYmgUaBdLAIWUaBmH
            lFKUKEsBSwFLAoaUaCGJXZQojANvbmWUjAN0d2+UZXSUYmVdlChoDWgPfZQoaBFoFGgX
            SwCFlGgZh5RSlChLAUsBhZRoIYldlGgmYXSUYmgpTnWGlFKUaA1oD32UKGgRaBRoF0sA
            hZRoGYeUUpQoSwFLAYWUaCGJXZRoJWF0lGJoKU51hpRSlGgNaA99lChoEWgUaBdLAIWU
            aBmHlFKUKEsBSwGFlGghiV2UaCdhdJRiaClOdYaUUpRlfZSMBjAuMTQuMZR9lCiMBGF4
            ZXOUaAqMBmJsb2Nrc5RdlCh9lCiMBnZhbHVlc5RoOIwIbWdyX2xvY3OUjAhidWlsdGlu
            c5SMBXNsaWNllJOUSwFLAksBh5RSlHV9lChodmhDaHdoeksASwFLAYeUUpR1fZQoaHZo
            TWh3aHpLAksDSwGHlFKUdWV1c3SUYowEX3R5cJSMCWRhdGFmcmFtZZSMCV9tZXRhZGF0
            YZRdlIwFYXR0cnOUfZSMBl9mbGFnc5R9lIwXYWxsb3dzX2R1cGxpY2F0ZV9sYWJlbHOU
            iHN1Yi4=
            """
        )
        got_df = pickle.loads(old_pickle)
        self.assertTrue(_WANT_DF.equals(got_df))

    def test_new_pickle(self):
        # Produced by pickling _WANT_DF with Pandas 1.5.3.
        new_pickle = base64.b64decode(
            """
            gASVSQMAAAAAAACMEXBhbmRhcy5jb3JlLmZyYW1llIwJRGF0YUZyYW1llJOUKYGUfZQo
            jARfbWdylIwecGFuZGFzLmNvcmUuaW50ZXJuYWxzLm1hbmFnZXJzlIwMQmxvY2tNYW5h
            Z2VylJOUjBZwYW5kYXMuX2xpYnMuaW50ZXJuYWxzlIwPX3VucGlja2xlX2Jsb2NrlJOU
            jBVudW1weS5jb3JlLm11bHRpYXJyYXmUjAxfcmVjb25zdHJ1Y3SUk5SMBW51bXB5lIwH
            bmRhcnJheZSTlEsAhZRDAWKUh5RSlChLAUsBSwKGlGgPjAVkdHlwZZSTlIwCaTiUiYiH
            lFKUKEsDjAE8lE5OTkr/////Sv////9LAHSUYolDEAEAAAAAAAAAAgAAAAAAAACUdJRi
            jAhidWlsdGluc5SMBXNsaWNllJOUSwBLAUsBh5RSlEsCh5RSlGgLaA5oEUsAhZRoE4eU
            UpQoSwFLAUsChpRoGIwCZjiUiYiHlFKUKEsDaBxOTk5K/////0r/////SwB0lGKJQxCa
            mZmZmZnxP5qZmZmZmQFAlHSUYmgiSwFLAksBh5RSlEsCh5RSlGgLaA5oEUsAhZRoE4eU
            UpQoSwFLAUsChpRoGIwCTziUiYiHlFKUKEsDjAF8lE5OTkr/////Sv////9LP3SUYold
            lCiMA29uZZSMA3R3b5RldJRiaCJLAksDSwGHlFKUSwKHlFKUh5RdlCiMGHBhbmRhcy5j
            b3JlLmluZGV4ZXMuYmFzZZSMCl9uZXdfSW5kZXiUk5RoSIwFSW5kZXiUk5R9lCiMBGRh
            dGGUaA5oEUsAhZRoE4eUUpQoSwFLA4WUaDuJXZQojAJudJSMA2ZsdJSMBXN0cm5nlGV0
            lGKMBG5hbWWUTnWGlFKUaEqMGXBhbmRhcy5jb3JlLmluZGV4ZXMucmFuZ2WUjApSYW5n
            ZUluZGV4lJOUfZQoaFhOjAVzdGFydJRLAIwEc3RvcJRLAowEc3RlcJRLAXWGlFKUZYaU
            UpSMBF90eXCUjAlkYXRhZnJhbWWUjAlfbWV0YWRhdGGUXZSMBWF0dHJzlH2UjAZfZmxh
            Z3OUfZSMF2FsbG93c19kdXBsaWNhdGVfbGFiZWxzlIhzdWIu
            """
        )
        got_df = pickle.loads(new_pickle)
        self.assertTrue(_WANT_DF.equals(got_df))
