"""Test for the unified ``tiledb.cloud.taskgraphs`` namespace."""

import datetime
import unittest
from typing import Tuple

import tiledb.cloud.taskgraphs as tg


class TaskGraphsTest(unittest.TestCase):
    def test_basic(self):
        grf = tg.Builder()
        year = grf.input("year")
        month = grf.input("month")
        day = grf.input("day")
        zone = grf.input("timezone", "Europe/Athens")

        as_date = grf.udf(datetime.date, tg.args(year, month, day))

        def to_instants(day: datetime.date, zone_name: str):
            import datetime

            from dateutil import tz

            tomorrow = day + datetime.timedelta(days=1)
            zone = tz.gettz(zone_name)

            midnight = datetime.time(tzinfo=zone)

            start_instant = datetime.datetime.combine(day, midnight)
            end_instant = datetime.datetime.combine(tomorrow, midnight)

            return start_instant, end_instant

        start_end = grf.udf(to_instants, tg.args(as_date, zone))

        def to_utc(times):
            import datetime

            return [t.astimezone(datetime.timezone.utc) for t in times]

        utc_start_end = grf.udf(to_utc, tg.args(start_end), name="normalize")
        length = grf.udf(
            lambda se: se[1] - se[0], tg.args(utc_start_end), name="length"
        )

        def format_info(start_end, zone, length):
            start, end = start_end
            return f"{start:%Y-%m-%d} to {end:%Y-%m-%d} in {zone} is {length}"

        grf.udf(
            format_info,
            tg.args(start_end, zone, length),
            result_format="json",
            name="output",
        )

        exec = tg.execute(grf, year=2022, month=3, day=27)
        exec.wait(30)
        self.assertEqual(exec.status, tg.Status.SUCCEEDED)
        self.assertEqual(datetime.timedelta(hours=23), exec.node(length).result())
        self.assertEqual(
            "2022-03-27 to 2022-03-28 in Europe/Athens is 23:00:00",
            exec.node("output").result(),
        )
