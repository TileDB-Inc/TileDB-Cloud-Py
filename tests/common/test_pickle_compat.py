import base64
import pickle
import unittest

import numpy as np
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

_WANT_NDARRAYBACKED = pd.DataFrame(
    {
        "timestamp": np.array(
            (27984459, 27996857, 27988084, 27983388, 27993584), dtype="datetime64[m]"
        ),
        "x": (10.5, 15.7, 19.0, 10.5, 16.7),
        "y": (3.94, 3.44, 3.75, 3.21, 3.91),
        "z": (9, -5, 4, 8, 7),
    }
)
# Additional verification that `xarrays` will work based on customer need.
_WANT_XARR = _WANT_NDARRAYBACKED.set_index(["x", "y", "timestamp"]).to_xarray()


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

    def test_old_pickle_ndarraybacked(self):
        # Pickle of _WANT_NDARRAYBACKED in Pandas 2.4.
        old_pickle = base64.b64decode(
            """
            gANjcGFuZGFzLmNvcmUuZnJhbWUKRGF0YUZyYW1lCnEAKYFxAX1xAihYBAAAAF9tZ3Jx
            A2NwYW5kYXMuY29yZS5pbnRlcm5hbHMubWFuYWdlcnMKQmxvY2tNYW5hZ2VyCnEEKYFx
            BShdcQYoY3BhbmRhcy5jb3JlLmluZGV4ZXMuYmFzZQpfbmV3X0luZGV4CnEHY3BhbmRh
            cy5jb3JlLmluZGV4ZXMuYmFzZQpJbmRleApxCH1xCShYBAAAAGRhdGFxCmNudW1weS5j
            b3JlLm11bHRpYXJyYXkKX3JlY29uc3RydWN0CnELY251bXB5Cm5kYXJyYXkKcQxLAIVx
            DUMBYnEOh3EPUnEQKEsBSwSFcRFjbnVtcHkKZHR5cGUKcRJYAgAAAE84cROJiIdxFFJx
            FShLA1gBAAAAfHEWTk5OSv////9K/////0s/dHEXYoldcRgoWAkAAAB0aW1lc3RhbXBx
            GVgBAAAAeHEaWAEAAAB5cRtYAQAAAHpxHGV0cR1iWAQAAABuYW1lcR5OdYZxH1JxIGgH
            Y3BhbmRhcy5jb3JlLmluZGV4ZXMucmFuZ2UKUmFuZ2VJbmRleApxIX1xIihoHk5YBQAA
            AHN0YXJ0cSNLAFgEAAAAc3RvcHEkSwVYBAAAAHN0ZXBxJUsBdYZxJlJxJ2VdcSgoaAto
            DEsAhXEpaA6HcSpScSsoSwFLAksFhnEsaBJYAgAAAGY4cS2JiIdxLlJxLyhLA1gBAAAA
            PHEwTk5OSv////9K/////0sAdHExYolDUAAAAAAAACVAZmZmZmZmL0AAAAAAAAAzQAAA
            AAAAACVAMzMzMzOzMECF61G4HoUPQIXrUbgehQtAAAAAAAAADkCuR+F6FK4JQEjhehSu
            Rw9AcTJ0cTNiaAtoDEsAhXE0aA6HcTVScTYoSwFLAUsFhnE3aBJYAgAAAGk4cTiJiIdx
            OVJxOihLA2gwTk5OSv////9K/////0sAdHE7YolDKAkAAAAAAAAA+/////////8EAAAA
            AAAAAAgAAAAAAAAABwAAAAAAAABxPHRxPWJoC2gMSwCFcT5oDodxP1JxQChLAUsBSwWG
            cUFoElgCAAAATThxQomIh3FDUnFEKEsEaDBOTk5K/////0r/////SwB9cUUoQwJuc3FG
            SwFLAUsBdHFHhnFIdHFJYolDKADIlhMIP00XAJi+IpbjTxcA4NO92AROFwCgHWGWBE0X
            AICa2vowTxdxSnRxS2JlXXFMKGgHaAh9cU0oaApoC2gMSwCFcU5oDodxT1JxUChLAUsC
            hXFRaBWJXXFSKGgaaBtldHFTYmgeTnWGcVRScVVoB2gIfXFWKGgKaAtoDEsAhXFXaA6H
            cVhScVkoSwFLAYVxWmgViV1xW2gcYXRxXGJoHk51hnFdUnFeaAdoCH1xXyhoCmgLaAxL
            AIVxYGgOh3FhUnFiKEsBSwGFcWNoFYldcWRoGWF0cWViaB5OdYZxZlJxZ2V9cWhYBgAA
            ADAuMTQuMXFpfXFqKFgEAAAAYXhlc3FraAZYBgAAAGJsb2Nrc3FsXXFtKH1xbihYBgAA
            AHZhbHVlc3FvaCtYCAAAAG1ncl9sb2NzcXBjYnVpbHRpbnMKc2xpY2UKcXFLAUsDSwGH
            cXJScXN1fXF0KGhvaDZocGhxSwNLBEsBh3F1UnF2dX1xdyhob2hAaHBocUsASwFLAYdx
            eFJxeXVldXN0cXpiWAQAAABfdHlwcXtYCQAAAGRhdGFmcmFtZXF8WAkAAABfbWV0YWRh
            dGFxfV1xflgFAAAAYXR0cnNxf31xgFgGAAAAX2ZsYWdzcYF9cYJYFwAAAGFsbG93c19k
            dXBsaWNhdGVfbGFiZWxzcYOIc3ViLg==
            """
        )
        got_df = pickle.loads(old_pickle)
        self.assertTrue(_WANT_NDARRAYBACKED.equals(got_df))

        # Pickle of _WANT_XARR in Pandas 2.4.
        old_pickle_xarr = base64.b64decode(
            """
            gANjeGFycmF5LmNvcmUuZGF0YXNldApEYXRhc2V0CnEAKYFxAU59cQIoWAYAAABfYXR0
            cnNxA31xBFgMAAAAX2Nvb3JkX25hbWVzcQVjYnVpbHRpbnMKc2V0CnEGXXEHKFgJAAAA
            dGltZXN0YW1wcQhYAQAAAHlxCVgBAAAAeHEKZYVxC1JxDFgFAAAAX2RpbXNxDX1xDiho
            CksEaAlLBWgISwV1WAkAAABfZW5jb2RpbmdxD31xEFgGAAAAX2Nsb3NlcRFOWAgAAABf
            aW5kZXhlc3ESfXETKGgKY3hhcnJheS5jb3JlLmluZGV4ZXMKUGFuZGFzSW5kZXgKcRQp
            gXEVTn1xFihYBQAAAGluZGV4cRdjcGFuZGFzLmNvcmUuaW5kZXhlcy5iYXNlCl9uZXdf
            SW5kZXgKcRhjcGFuZGFzLmNvcmUuaW5kZXhlcy5udW1lcmljCkZsb2F0NjRJbmRleApx
            GX1xGihYBAAAAGRhdGFxG2NudW1weS5jb3JlLm11bHRpYXJyYXkKX3JlY29uc3RydWN0
            CnEcY251bXB5Cm5kYXJyYXkKcR1LAIVxHkMBYnEfh3EgUnEhKEsBSwSFcSJjbnVtcHkK
            ZHR5cGUKcSNYAgAAAGY4cSSJiIdxJVJxJihLA1gBAAAAPHEnTk5OSv////9K/////0sA
            dHEoYolDIAAAAAAAACVAZmZmZmZmL0AzMzMzM7MwQAAAAAAAADNAcSl0cSpiWAQAAABu
            YW1lcStoCnWGcSxScS1YAwAAAGRpbXEuaAp1hnEvYmgJaBQpgXEwTn1xMShoF2gYaBl9
            cTIoaBtoHGgdSwCFcTNoH4dxNFJxNShLAUsFhXE2aCaJQyiuR+F6FK4JQIXrUbgehQtA
            AAAAAAAADkBI4XoUrkcPQIXrUbgehQ9AcTd0cThiaCtoCXWGcTlScTpoLmgJdYZxO2Jo
            CGgUKYFxPE59cT0oaBdjcGFuZGFzLmNvcmUuaW5kZXhlcy5kYXRldGltZXMKX25ld19E
            YXRldGltZUluZGV4CnE+Y3BhbmRhcy5jb3JlLmluZGV4ZXMuZGF0ZXRpbWVzCkRhdGV0
            aW1lSW5kZXgKcT99cUAoaBtjcGFuZGFzLmNvcmUuYXJyYXlzLmRhdGV0aW1lcwpEYXRl
            dGltZUFycmF5CnFBKYFxQn1xQyhYBQAAAF9kYXRhcURoHGgdSwCFcUVoH4dxRlJxRyhL
            AUsFhXFIaCNYAgAAAE04cUmJiIdxSlJxSyhLBGgnTk5OSv////9K/////0sAfXFMKEMC
            bnNxTUsBSwFLAXRxToZxT3RxUGKJQygAoB1hlgRNFwDIlhMIP00XAODTvdgEThcAgJra
            +jBPFwCYviKW408XcVF0cVJiWAUAAABfZnJlcXFTTlgGAAAAX2R0eXBlcVRoI1gCAAAA
            TThxVYmIh3FWUnFXKEsEaCdOTk5K/////0r/////SwB9cVgoQwJuc3FZSwFLAUsBdHFa
            hnFbdHFcYlgGAAAAX2NhY2hlcV19cV5YCAAAAF9uZGFycmF5cV9oR3N1YmgraAhYAgAA
            AHR6cWBOWAQAAABmcmVxcWFOdYZxYlJxY2guaAh1hnFkYnVYCgAAAF92YXJpYWJsZXNx
            ZX1xZihoCmN4YXJyYXkuY29yZS52YXJpYWJsZQpJbmRleFZhcmlhYmxlCnFnKYFxaE59
            cWkoaA1oCoVxamhEY3hhcnJheS5jb3JlLmluZGV4aW5nClBhbmRhc0luZGV4aW5nQWRh
            cHRlcgpxaymBcWxOfXFtKFgFAAAAYXJyYXlxbmgYaBl9cW8oaBtoIWgraAp1hnFwUnFx
            aFRoJnWGcXJiaAN9cXNoD051hnF0YmgJaGcpgXF1Tn1xdihoDWgJhXF3aERoaymBcXhO
            fXF5KGhuaBhoGX1xeihoG2g1aCtoCXWGcXtScXxoVGgmdYZxfWJoA31xfmgPTnWGcX9i
            aAhoZymBcYBOfXGBKGgNaAiFcYJoRGhrKYFxg059cYQoaG5oPmg/fXGFKGgbaEJoK2gI
            aGBOaGFOdYZxhlJxh2hUaFd1hnGIYmgDfXGJaA9OdYZximJYAQAAAHpxi2N4YXJyYXku
            Y29yZS52YXJpYWJsZQpWYXJpYWJsZQpxjCmBcY1OfXGOKGgNaApoCWgIh3GPaERoHGgd
            SwCFcZBoH4dxkVJxkihLAUsESwVLBYdxk2gmiUIgAwAAAAAAAAAAIEAAAAAAAAD4fwAA
            AAAAAPh/AAAAAAAA+H8AAAAAAAD4fwAAAAAAAPh/AAAAAAAA+H8AAAAAAAD4fwAAAAAA
            APh/AAAAAAAA+H8AAAAAAAD4fwAAAAAAAPh/AAAAAAAA+H8AAAAAAAD4fwAAAAAAAPh/
            AAAAAAAA+H8AAAAAAAD4fwAAAAAAAPh/AAAAAAAA+H8AAAAAAAD4fwAAAAAAAPh/AAAA
            AAAAIkAAAAAAAAD4fwAAAAAAAPh/AAAAAAAA+H8AAAAAAAD4fwAAAAAAAPh/AAAAAAAA
            +H8AAAAAAAD4fwAAAAAAAPh/AAAAAAAA+H8AAAAAAAD4fwAAAAAAAPh/AAAAAAAA+H8A
            AAAAAAAUwAAAAAAAAPh/AAAAAAAA+H8AAAAAAAD4fwAAAAAAAPh/AAAAAAAA+H8AAAAA
            AAD4fwAAAAAAAPh/AAAAAAAA+H8AAAAAAAD4fwAAAAAAAPh/AAAAAAAA+H8AAAAAAAD4
            fwAAAAAAAPh/AAAAAAAA+H8AAAAAAAD4fwAAAAAAAPh/AAAAAAAA+H8AAAAAAAD4fwAA
            AAAAAPh/AAAAAAAA+H8AAAAAAAD4fwAAAAAAAPh/AAAAAAAA+H8AAAAAAAD4fwAAAAAA
            APh/AAAAAAAA+H8AAAAAAAD4fwAAAAAAAPh/AAAAAAAA+H8AAAAAAAD4fwAAAAAAAPh/
            AAAAAAAA+H8AAAAAAAD4fwAAAAAAABxAAAAAAAAA+H8AAAAAAAD4fwAAAAAAAPh/AAAA
            AAAA+H8AAAAAAAD4fwAAAAAAAPh/AAAAAAAA+H8AAAAAAAD4fwAAAAAAAPh/AAAAAAAA
            +H8AAAAAAAD4fwAAAAAAAPh/AAAAAAAA+H8AAAAAAAD4fwAAAAAAAPh/AAAAAAAA+H8A
            AAAAAAD4fwAAAAAAAPh/AAAAAAAAEEAAAAAAAAD4fwAAAAAAAPh/AAAAAAAA+H8AAAAA
            AAD4fwAAAAAAAPh/AAAAAAAA+H8AAAAAAAD4fwAAAAAAAPh/AAAAAAAA+H8AAAAAAAD4
            fwAAAAAAAPh/AAAAAAAA+H9xlHRxlWJoA31xlmgPTnWGcZdidXWGcZhiLg==
            """
        )
        got_xarr = pickle.loads(old_pickle_xarr)
        self.assertTrue(_WANT_XARR.equals(got_xarr))

    def test_new_pickle_ndarraybacked(self):
        # Pickle of _WANT_NDARRAYBACKED in Pandas 1.5.3.
        new_pickle = base64.b64decode(
            """
            gASVrAQAAAAAAACMEXBhbmRhcy5jb3JlLmZyYW1llIwJRGF0YUZyYW1llJOUKYGUfZQo
            jARfbWdylIwecGFuZGFzLmNvcmUuaW50ZXJuYWxzLm1hbmFnZXJzlIwMQmxvY2tNYW5h
            Z2VylJOUjBZwYW5kYXMuX2xpYnMuaW50ZXJuYWxzlIwPX3VucGlja2xlX2Jsb2NrlJOU
            jBNwYW5kYXMuX2xpYnMuYXJyYXlzlIwcX19weXhfdW5waWNrbGVfTkRBcnJheUJhY2tl
            ZJSTlIwccGFuZGFzLmNvcmUuYXJyYXlzLmRhdGV0aW1lc5SMDURhdGV0aW1lQXJyYXmU
            k5RKuFxVDU6HlFKUjAVudW1weZSMBWR0eXBllJOUjAJNOJSJiIeUUpQoSwSMATyUTk5O
            Sv////9K/////0sAfZQoQwJuc5RLAUsBSwF0lIaUdJRijBVudW1weS5jb3JlLm11bHRp
            YXJyYXmUjAxfcmVjb25zdHJ1Y3SUk5RoFIwHbmRhcnJheZSTlEsAhZRDAWKUh5RSlChL
            AUsBSwWGlGgWjAJNOJSJiIeUUpQoSwRoGk5OTkr/////Sv////9LAH2UKEMCbnOUSwFL
            AUsBdJSGlHSUYolDKADIlhMIP00XAJi+IpbjTxcA4NO92AROFwCgHWGWBE0XAICa2vow
            TxeUdJRifZSMBV9mcmVxlE5zh5RijAhidWlsdGluc5SMBXNsaWNllJOUSwBLAUsBh5RS
            lEsCh5RSlGgLaCJoJEsAhZRoJoeUUpQoSwFLAksFhpRoFowCZjiUiYiHlFKUKEsDaBpO
            Tk5K/////0r/////SwB0lGKJQ1AAAAAAAAAlQGZmZmZmZi9AAAAAAAAAM0AAAAAAAAAl
            QDMzMzMzszBAhetRuB6FD0CF61G4HoULQAAAAAAAAA5ArkfhehSuCUBI4XoUrkcPQJR0
            lGJoOUsBSwNLAYeUUpRLAoeUUpRoC2giaCRLAIWUaCaHlFKUKEsBSwFLBYaUaBaMAmk4
            lImIh5RSlChLA2gaTk5OSv////9K/////0sAdJRiiUMoCQAAAAAAAAD7/////////wQA
            AAAAAAAACAAAAAAAAAAHAAAAAAAAAJR0lGJoOUsDSwRLAYeUUpRLAoeUUpSHlF2UKIwY
            cGFuZGFzLmNvcmUuaW5kZXhlcy5iYXNllIwKX25ld19JbmRleJSTlGhcjAVJbmRleJST
            lH2UKIwEZGF0YZRoImgkSwCFlGgmh5RSlChLAUsEhZRoFowCTziUiYiHlFKUKEsDjAF8
            lE5OTkr/////Sv////9LP3SUYoldlCiMCXRpbWVzdGFtcJSMAXiUjAF5lIwBepRldJRi
            jARuYW1llE51hpRSlGhejBlwYW5kYXMuY29yZS5pbmRleGVzLnJhbmdllIwKUmFuZ2VJ
            bmRleJSTlH2UKGhyTowFc3RhcnSUSwCMBHN0b3CUSwWMBHN0ZXCUSwF1hpRSlGWGlFKU
            jARfdHlwlIwJZGF0YWZyYW1llIwJX21ldGFkYXRhlF2UjAVhdHRyc5R9lIwGX2ZsYWdz
            lH2UjBdhbGxvd3NfZHVwbGljYXRlX2xhYmVsc5SIc3ViLg==
            """
        )
        got_df = pickle.loads(new_pickle)
        self.assertTrue(_WANT_NDARRAYBACKED.equals(got_df))

        # Pickle of _WANT_XARR in Pandas 1.2.4.
        new_pickle_xarr = base64.b64decode(
            """
            gASV4AgAAAAAAACME3hhcnJheS5jb3JlLmRhdGFzZXSUjAdEYXRhc2V0lJOUKYGUTn2U
            KIwGX2F0dHJzlH2UjAxfY29vcmRfbmFtZXOUj5QojAF5lIwJdGltZXN0YW1wlIwBeJSQ
            jAVfZGltc5R9lChoC0sEaAlLBWgKSwV1jAlfZW5jb2RpbmeUfZSMBl9jbG9zZZROjAhf
            aW5kZXhlc5R9lChoC4wTeGFycmF5LmNvcmUuaW5kZXhlc5SMC1BhbmRhc0luZGV4lJOU
            KYGUTn2UKIwFaW5kZXiUjBhwYW5kYXMuY29yZS5pbmRleGVzLmJhc2WUjApfbmV3X0lu
            ZGV4lJOUjBtwYW5kYXMuY29yZS5pbmRleGVzLm51bWVyaWOUjAxGbG9hdDY0SW5kZXiU
            k5R9lCiMBGRhdGGUjBVudW1weS5jb3JlLm11bHRpYXJyYXmUjAxfcmVjb25zdHJ1Y3SU
            k5SMBW51bXB5lIwHbmRhcnJheZSTlEsAhZRDAWKUh5RSlChLAUsEhZRoJIwFZHR5cGWU
            k5SMAmY4lImIh5RSlChLA4wBPJROTk5K/////0r/////SwB0lGKJQyAAAAAAAAAlQGZm
            ZmZmZi9AMzMzMzOzMEAAAAAAAAAzQJR0lGKMBG5hbWWUaAt1hpRSlIwDZGltlGgLjAtj
            b29yZF9kdHlwZZRoMHWGlGJoCWgVKYGUTn2UKGgYaBtoHn2UKGggaCNoJksAhZRoKIeU
            UpQoSwFLBYWUaDCJQyiuR+F6FK4JQIXrUbgehQtAAAAAAAAADkBI4XoUrkcPQIXrUbge
            hQ9AlHSUYmg1aAl1hpRSlGg4aAloOWgwdYaUYmgKaBUpgZROfZQoaBiMHXBhbmRhcy5j
            b3JlLmluZGV4ZXMuZGF0ZXRpbWVzlIwSX25ld19EYXRldGltZUluZGV4lJOUaEmMDURh
            dGV0aW1lSW5kZXiUk5R9lChoIIwTcGFuZGFzLl9saWJzLmFycmF5c5SMHF9fcHl4X3Vu
            cGlja2xlX05EQXJyYXlCYWNrZWSUk5SMHHBhbmRhcy5jb3JlLmFycmF5cy5kYXRldGlt
            ZXOUjA1EYXRldGltZUFycmF5lJOUSrhcVQ1Oh5RSlGgtjAJNOJSJiIeUUpQoSwRoMU5O
            Tkr/////Sv////9LAH2UKEMCbnOUSwFLAUsBdJSGlHSUYmgjaCZLAIWUaCiHlFKUKEsB
            SwWFlGgtjAJNOJSJiIeUUpQoSwRoMU5OTkr/////Sv////9LAH2UKEMCbnOUSwFLAUsB
            dJSGlHSUYolDKACgHWGWBE0XAMiWEwg/TRcA4NO92AROFwCAmtr6ME8XAJi+IpbjTxeU
            dJRifZSMBV9mcmVxlE5zh5RiaDVoCnWGlFKUaDhoCmg5aFl1hpRidYwKX3ZhcmlhYmxl
            c5R9lChoC4wUeGFycmF5LmNvcmUudmFyaWFibGWUjA1JbmRleFZhcmlhYmxllJOUKYGU
            Tn2UKGgMaAuFlIwFX2RhdGGUjBR4YXJyYXkuY29yZS5pbmRleGluZ5SMFVBhbmRhc0lu
            ZGV4aW5nQWRhcHRlcpSTlCmBlE59lCiMBWFycmF5lGgbaB59lChoIGgqaDVoC3WGlFKU
            jAZfZHR5cGWUaDB1hpRiaAV9lGgOfZR1hpRiaAlodymBlE59lChoDGgJhZRoe2h+KYGU
            Tn2UKGiBaBtoHn2UKGggaEBoNWgJdYaUUpRohWgwdYaUYmgFfZRoDn2UdYaUYmgKaHcp
            gZROfZQoaAxoCoWUaHtofimBlE59lChogWhLaE19lChoIGhWaDVoCnWGlFKUaIVoWXWG
            lGJoBX2UaA59lHWGlGKMAXqUaHWMCFZhcmlhYmxllJOUKYGUTn2UKGgMaAtoCWgKh5Ro
            e2gjaCZLAIWUaCiHlFKUKEsBSwRLBUsFh5RoMIlCIAMAAAAAAAAAACBAAAAAAAAA+H8A
            AAAAAAD4fwAAAAAAAPh/AAAAAAAA+H8AAAAAAAD4fwAAAAAAAPh/AAAAAAAA+H8AAAAA
            AAD4fwAAAAAAAPh/AAAAAAAA+H8AAAAAAAD4fwAAAAAAAPh/AAAAAAAA+H8AAAAAAAD4
            fwAAAAAAAPh/AAAAAAAA+H8AAAAAAAD4fwAAAAAAAPh/AAAAAAAA+H8AAAAAAAD4fwAA
            AAAAACJAAAAAAAAA+H8AAAAAAAD4fwAAAAAAAPh/AAAAAAAA+H8AAAAAAAD4fwAAAAAA
            APh/AAAAAAAA+H8AAAAAAAD4fwAAAAAAAPh/AAAAAAAA+H8AAAAAAAD4fwAAAAAAAPh/
            AAAAAAAAFMAAAAAAAAD4fwAAAAAAAPh/AAAAAAAA+H8AAAAAAAD4fwAAAAAAAPh/AAAA
            AAAA+H8AAAAAAAD4fwAAAAAAAPh/AAAAAAAA+H8AAAAAAAD4fwAAAAAAAPh/AAAAAAAA
            +H8AAAAAAAD4fwAAAAAAAPh/AAAAAAAA+H8AAAAAAAD4fwAAAAAAAPh/AAAAAAAA+H8A
            AAAAAAD4fwAAAAAAAPh/AAAAAAAA+H8AAAAAAAD4fwAAAAAAAPh/AAAAAAAA+H8AAAAA
            AAD4fwAAAAAAAPh/AAAAAAAA+H8AAAAAAAD4fwAAAAAAAPh/AAAAAAAA+H8AAAAAAAD4
            fwAAAAAAAPh/AAAAAAAA+H8AAAAAAAAcQAAAAAAAAPh/AAAAAAAA+H8AAAAAAAD4fwAA
            AAAAAPh/AAAAAAAA+H8AAAAAAAD4fwAAAAAAAPh/AAAAAAAA+H8AAAAAAAD4fwAAAAAA
            APh/AAAAAAAA+H8AAAAAAAD4fwAAAAAAAPh/AAAAAAAA+H8AAAAAAAD4fwAAAAAAAPh/
            AAAAAAAA+H8AAAAAAAD4fwAAAAAAABBAAAAAAAAA+H8AAAAAAAD4fwAAAAAAAPh/AAAA
            AAAA+H8AAAAAAAD4fwAAAAAAAPh/AAAAAAAA+H8AAAAAAAD4fwAAAAAAAPh/AAAAAAAA
            +H8AAAAAAAD4fwAAAAAAAPh/lHSUYmgFfZRoDk51hpRidXWGlGIu
            """
        )
        got_xarr = pickle.loads(new_pickle_xarr)
        self.assertTrue(_WANT_XARR.equals(got_xarr))
