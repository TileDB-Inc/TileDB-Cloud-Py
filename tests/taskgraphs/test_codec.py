import datetime
import json
import unittest

from tiledb.cloud.taskgraphs import _codec


class TestUnescaper(unittest.TestCase):
    def test_unescaping(self):
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
                """,
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
                """,
                range(666),
            ),
        )

        for name, inp, expected in cases:
            with self.subTest(name):
                decoded_input = json.loads(inp)
                unesc = _codec.Unescaper()
                actual = unesc.visit(decoded_input)
                self.assertEqual(expected, actual)
