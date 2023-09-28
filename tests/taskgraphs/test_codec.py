import datetime
import json
import unittest

import pyarrow
import urllib3

from tiledb.cloud._results import codecs
from tiledb.cloud._results import tiledb_json


class EscapingTest(unittest.TestCase):
    def test_bidirectional(self):
        cases = (
            (
                "simple",
                '{"here": "there"}',
                {"here": "there"},
            ),
            (
                "nested pickle",
                """
                    {
                      "__tdbudf__": "__escape__",
                      "__escape__": {
                        "a": "b",
                        "__tdbudf__": {
                          "__tdbudf__": "immediate",
                          "format": "python_pickle",
                          "base64_data": "gASVEgAAAAAAAACMBGpzb26UjAVsb2Fkc5STlC4="
                        }
                      }
                    }
                """,
                {
                    "a": "b",
                    "__tdbudf__": json.loads,
                },
            ),
            (
                "complex",
                """
                    {
                      "__tdbudf__": "__escape__",
                      "__escape__": {
                        "c": "d",
                        "__tdbudf__": {
                          "__tdbudf__": "__escape__",
                          "__escape__": {
                            "e": null,
                            "__tdbudf__": 6,
                            "f": {
                              "__tdbudf__": "immediate",
                              "format": "bytes",
                              "base64_data": "YXNkbGtmamFzZGxm"
                            },
                            "g": [
                              "here",
                              "there",
                              "everywhere",
                              {
                                "__tdbudf__": "immediate",
                                "format": "python_pickle",
                                "base64_data": "gASVNwAAAAAAAACMCGRhdGV0aW1llIwIdGltZXpvbmWUk5RoAIwJdGltZWRlbHRhlJOUSwBLAEsAh5RSlIWUUpQu"
                              },
                              {
                                "__tdbudf__": "immediate",
                                "format": "python_pickle",
                                "base64_data": "gASVFAAAAAAAAACMCGJ1aWx0aW5zlIwDbGVulJOULg=="
                              }
                            ]
                          }
                        }
                      }
                    }
                """,  # noqa: E501
                {
                    "c": "d",
                    "__tdbudf__": {
                        "e": None,
                        "__tdbudf__": 6,
                        "f": b"asdlkfjasdlf",
                        "g": [
                            "here",
                            "there",
                            "everywhere",
                            datetime.timezone.utc,
                            len,
                        ],
                    },
                },
            ),
            (
                "just a range",
                """
                    {
                      "__tdbudf__": "immediate",
                      "format": "python_pickle",
                      "base64_data": "gASVIQAAAAAAAACMCGJ1aWx0aW5zlIwFcmFuZ2WUk5RLAE2aAksBh5RSlC4="
                    }
                """,  # noqa: E501
                range(666),
            ),
        )

        for name, json_text, native_value in cases:
            json_data = json.loads(json_text)
            with self.subTest(f"unescaping {name}"):
                unesc = tiledb_json.Decoder()
                actual = unesc.visit(json_data)
                self.assertEqual(native_value, actual)

            with self.subTest(f"escaping {name}"):
                esc = tiledb_json.Encoder()
                actual = esc.visit(native_value)
                self.assertEqual(json_data, actual)

    def test_raw_json(self):
        """Verifies that visiting ``raw_json`` nodes short-circuits."""
        basic_case = {
            "__tdbudf__": "raw_json",
            "raw_json": {
                "__tdbudf__": "who-cares",
                "dont-visit-me": "hello",
            },
        }

        me = self

        class DontVisitVerifier(tiledb_json.Decoder):
            def visit(self, value: object):
                if isinstance(value, dict):
                    me.assertNotIn("dont-visit-me", value)
                return super().visit(value)

        dec = DontVisitVerifier()
        actual = dec.visit(basic_case)
        self.assertEqual(
            {
                "__tdbudf__": "who-cares",
                "dont-visit-me": "hello",
            },
            actual,
        )


class BinaryResultTest(unittest.TestCase):
    def test_binary_result_of(self):
        cases = (
            (b"possession", codecs.BinaryBlob("bytes", b"possession")),
            (
                frozenset(),
                codecs.BinaryBlob(
                    "python_pickle",
                    b"\x80\x04\x95\x04\x00\x00\x00\x00\x00\x00\x00(\x91\x94.",
                ),
            ),
            (pyarrow.Table.from_pydict({}), codecs.BinaryBlob("arrow", b"")),
        )
        for inval, expected in cases:
            with self.subTest(inval):
                self.assertEqual(expected, codecs.BinaryBlob.of(inval))

    def test_from_response(self):
        cases = [
            dict(
                mime="application/octet-stream",
                data=b"raw bytes",
                want_format="bytes",
                want_output=b"raw bytes",
            ),
            dict(
                mime="application/json",
                data=b'{"here": "there"}',
                want_format="json",
                want_output={"here": "there"},
            ),
            dict(
                mime="application/vnd.tiledb.python-pickle",
                data=b"\x80\x04\x95\x04\x00\x00\x00\x00\x00\x00\x00(\x91\x94.",
                want_format="python_pickle",
                want_output=frozenset(),
            ),
            dict(
                mime="unknown/mime",
                data=b"bogus data",
                want_format="mime:unknown/mime",
            ),
        ]
        for case in cases:
            with self.subTest(case["mime"]):
                resp = urllib3.HTTPResponse(
                    body=case["data"],
                    headers={"Content-Type": case["mime"]},
                )
                actual = codecs.BinaryBlob.from_response(resp)
                self.assertEqual(case["want_format"], actual.format)
                try:
                    want_out = case["want_output"]
                except KeyError:
                    pass
                else:
                    self.assertEqual(want_out, actual.decode())


class JSONableTest(unittest.TestCase):
    def test_yes(self):
        cases = [
            "I'm a string",
            1234,
            999.999,
            True,
            dict(),
            None,
            {"string key": frozenset()},
            ["a", len],
            (),
        ]
        for case in cases:
            with self.subTest(case):
                self.assertTrue(tiledb_json.is_jsonable_shallow(case))

    def test_no(self):
        cases = [
            b"i am bytes",
            set(),
            {b"non-string key": object()},
            object(),
            range(1000),
            complex(1, 2),
            Ellipsis,
        ]
        for case in cases:
            with self.subTest(case):
                self.assertFalse(tiledb_json.is_jsonable_shallow(case))
