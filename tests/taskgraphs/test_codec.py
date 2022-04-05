import datetime
import json
import unittest

from tiledb.cloud.taskgraphs import _codec


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

        for name, json_text, native_value in cases:
            json_data = json.loads(json_text)
            with self.subTest(f"unescaping {name}"):
                unesc = _codec.Unescaper()
                actual = unesc.visit(json_data)
                self.assertEqual(native_value, actual)

            with self.subTest(f"escaping {name}"):
                esc = _codec.Escaper()
                actual = esc.visit(native_value)
                self.assertEqual(json_data, actual)

    def test_json_encodable(self):
        data = _codec.BinaryResult("bytes", b"now")
        esc = _codec.Escaper()
        in_data = ["one", data, 2]
        expected = [
            "one",
            {"__tdbudf__": "immediate", "format": "bytes", "base64_data": "bm93"},
            2,
        ]
        self.assertEqual(expected, esc.visit(in_data))


class BinaryResultTest(unittest.TestCase):
    def test_binary_result_of(self):
        cases = (
            (b"possession", _codec.BinaryResult("bytes", b"possession")),
            (
                frozenset(),
                _codec.BinaryResult(
                    "python_pickle",
                    b"\x80\x04\x95\x04\x00\x00\x00\x00\x00\x00\x00(\x91\x94.",
                ),
            ),
        )
        for inval, expected in cases:
            with self.subTest(inval):
                self.assertEqual(expected, _codec.BinaryResult.of(inval))


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
                self.assertTrue(_codec.is_jsonable_shallow(case))

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
                self.assertFalse(_codec.is_jsonable_shallow(case))
