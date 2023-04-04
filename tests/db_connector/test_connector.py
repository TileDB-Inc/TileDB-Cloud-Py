import os
import unittest

from tiledb.cloud.sql.tiledb_connection import TileDBConnection


class TileDBConnectionTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # Using setUpClass to run query only once for this class
        con = TileDBConnection()
        cls.cur = con.cursor()
        cls.cur.execute(
            "SELECT * from `tiledb://TileDB-Inc/quickstart_dense` WHERE `rows` > ?",
            (0,),
        )
        cls.correct_data = [
            {"rows": 1, "cols": 1, "a": 1},
            {"rows": 1, "cols": 2, "a": 2},
            {"rows": 1, "cols": 3, "a": 3},
            {"rows": 1, "cols": 4, "a": 4},
            {"rows": 2, "cols": 1, "a": 5},
            {"rows": 2, "cols": 2, "a": 6},
            {"rows": 2, "cols": 3, "a": 7},
            {"rows": 2, "cols": 4, "a": 8},
            {"rows": 3, "cols": 1, "a": 9},
            {"rows": 3, "cols": 2, "a": 10},
            {"rows": 3, "cols": 3, "a": 11},
            {"rows": 3, "cols": 4, "a": 12},
            {"rows": 4, "cols": 1, "a": 13},
            {"rows": 4, "cols": 2, "a": 14},
            {"rows": 4, "cols": 3, "a": 15},
            {"rows": 4, "cols": 4, "a": 16},
        ]

    def test_row_count(self):
        # reset the cursor
        self.cur.scroll(0, "absolute")
        self.assertEqual(16, self.cur.rowcount)

    def test_fetchall(self):
        # reset the cursor
        self.cur.scroll(0, "absolute")
        results = self.cur.fetchall()
        self.assertEqual(results, self.correct_data)

    def test_fetchmany(self):
        self.cur.scroll(0, "absolute")
        results = self.cur.fetchmany(5)
        self.assertEqual(results, self.correct_data[:5])
        results = self.cur.fetchmany(2)
        self.assertEqual(results, self.correct_data[5:7])

    def test_fetchone(self):
        self.cur.scroll(1, "absolute")
        results = self.cur.fetchone()
        self.assertEqual(results, self.correct_data[1])

    def test_fetchmix(self):
        self.cur.scroll(0, "absolute")
        results = self.cur.fetchmany(5)
        self.assertEqual(results, self.correct_data[:5])
        results = self.cur.fetchone()
        self.assertEqual(results, self.correct_data[5])
        results = self.cur.fetchall()
        self.assertEqual(results, self.correct_data[6:])

    def test_description(self):
        correct_description = [
            ("rows", "NUMBER", None, None, None, None, None),
            ("cols", "NUMBER", None, None, None, None, None),
            ("a", "NUMBER", None, None, None, None, None),
        ]
        self.cur.scroll(0, "absolute")
        desc = self.cur.description
        self.assertEqual(desc, correct_description)
