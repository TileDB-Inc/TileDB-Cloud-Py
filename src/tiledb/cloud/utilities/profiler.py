import inspect
import subprocess
import threading
import time
from typing import Any, Optional

import numpy as np
from typing_extensions import Self

import tiledb
from tiledb.cloud.utilities import max_memory_usage
from tiledb.cloud.utilities import read_file


def create_log_array(uri: str) -> None:
    """
    Create an array to hold log events.

    :param uri: array URI
    """

    int_fl = tiledb.FilterList(
        [
            tiledb.DoubleDeltaFilter(),
            tiledb.BitWidthReductionFilter(),
            tiledb.ZstdFilter(),
        ]
    )
    ascii_fl = tiledb.FilterList([tiledb.ZstdFilter()])

    max_time = np.iinfo(np.uint64).max - 1
    d0 = tiledb.Dim(
        name="time_ms", dtype=np.uint64, domain=(0, max_time), filters=int_fl
    )
    dom = tiledb.Domain([d0])

    schema = tiledb.ArraySchema(
        domain=dom,
        sparse=True,
        attrs=[
            tiledb.Attr(name="id", dtype="ascii", filters=ascii_fl),
            tiledb.Attr(name="op", dtype="ascii", filters=ascii_fl),
            tiledb.Attr(name="data", dtype="ascii", filters=ascii_fl),
            tiledb.Attr(name="extra", dtype="ascii", filters=ascii_fl),
        ],
        offsets_filters=int_fl,
        allows_duplicates=True,
    )

    schema.check()
    tiledb.Array.create(uri, schema)


def write_log_event(
    uri: str,
    id: str,
    op: Optional[str] = "",
    data: Optional[str] = "",
    extra: Optional[str] = "",
) -> None:
    """
    Write an event to the log array.

    When writing large amounts of data, store the data in the `extra` parameter
    to improve query performance when the `extra` data is not needed.

    :param uri: array URI
    :param id: event id
    :param op: event operation, defaults to ""
    :param data: event data, defaults to ""
    :param extra: event extra data, defaults to ""
    """

    t_now_ms = time.time() * 1000
    with tiledb.open(uri, "w") as A:
        A[t_now_ms] = {
            "id": [id],
            "op": [op],
            "data": [data],
            "extra": [extra],
        }


class Profiler(object):
    """
    A context manager–based profiler to log events and CPU and memory usage
    to a TileDB array.

    If the `trace` parameter is `True`, CPU and memory usage will be logged to the array
    every `period_sec` seconds. This is useful for profiling jobs that are OOM killed.

    Examples:

        # Basic usage
        with Profiler(array_uri="tiledb://array-uri..."):
            # code to profile

        # Write custom events
        with Profiler(group_uri="tiledb://group-uri...", group_member="log") as prof:
            # code to profile

            # write custom event
            prof.write("my-op", "my-data", "my-extra-data")

            # more code to profile

    """

    def __init__(
        self,
        *,
        array_uri: Optional[str] = None,
        group_uri: Optional[str] = None,
        group_member: Optional[str] = None,
        id: Optional[str] = None,
        period_sec: int = 5,
        trace: bool = False,
    ):
        """
        Create a profiler object which logs events to a TileDB array. The array can be
        specified by URI or by group URI and group member name.

        :param array_uri: URI of the log array, defaults to None
        :param group_uri: URI of the group containing the log array, defaults to None
        :param group_member: group member name of the log array, defaults to None
        :param id: profiler id, written to event id
        :param period_sec: profiling period in seconds (0 = disabled), defaults to 5
        :param trace: enable trace logging, defaults to False
        """

        if array_uri is None and group_uri is None:
            self.enabled = False
            return

        self.enabled = True
        if array_uri is not None and group_uri is not None:
            raise ValueError("array_uri and group_uri cannot both be specified")
        if group_uri is not None and group_member is None:
            raise ValueError("group_member must be specified")

        if group_uri is not None:
            try:
                with tiledb.Group(group_uri) as group:
                    self.array_uri = group[group_member].uri
            except Exception:
                # Disable the profiler if we cannot access the group or member.
                self.enabled = False
                return
        else:
            self.array_uri = array_uri

        self.id = id or inspect.stack()[1].function
        self.period_sec = period_sec
        self.trace = trace

    def __enter__(self) -> Self:
        if not self.enabled:
            return self

        self.array = tiledb.open(self.array_uri, "w")

        # Log useful system info
        node_id = read_file("/proc/sys/kernel/random/boot_id")

        commands = (
            ("uptime"),
            ("free", "-h"),
            ("uname", "-a"),
            ("lscpu"),
        )

        node_info = ""
        for command in commands:
            output = subprocess.run(
                command, capture_output=True, text=True
            ).stdout.strip()
            node_info += output + "\n"

        self.write("start", node_id, node_info)

        self.t_start = time.time()
        if self.period_sec:
            # Start profiling timer
            self.done = False
            self.t_next = self.t_start
            self.stats = ["time,cpu,mem"]
            self._timeout()

        return self

    def __exit__(self, *_: Any) -> None:
        if not self.enabled:
            return

        # Write finish event with elapsed time
        t_elapsed = time.time() - self.t_start
        self.write("finish", f"{t_elapsed:.3f}")

        # Stop profiling timer and write stats event with max memory usage
        # and profiling stats
        self.done = True
        mem = max_memory_usage()
        extra = "\n".join(self.stats) if self.period_sec else ""
        self.write("stats", mem, extra)
        self.array.close()

    def write(self, op: str = "", data: str = "", extra: str = "") -> None:
        """
        Write an event to the log array.

        When writing large amounts of data, store the data in the `extra` parameter
        to improve query performance when the `extra` data is not needed.

        :param op: event op, defaults to ""
        :param data: event data, defaults to ""
        :param extra: event extra data, defaults to ""
        """

        if not self.enabled:
            return

        t_now_ms = time.time() * 1000

        if not self.array_uri:
            print(f"{t_now_ms},{self.id},{op},{data},{extra}")
            return

        self.array[t_now_ms] = {
            "id": [self.id],
            "op": [op],
            "data": [data],
            "extra": [extra],
        }

    def _timeout(self) -> None:
        """
        Capture system stats and schedule the next timeout.
        """

        try:
            cpu = read_file("/sys/fs/cgroup/cpu/cpuacct.usage")
            mem = read_file("/sys/fs/cgroup/memory/memory.usage_in_bytes")
        except Exception:
            cpu = 0
            mem = 0

        t_now = time.time()
        self.stats.append(f"{int(t_now)},{cpu},{mem}")

        if self.trace:
            self.write("trace", cpu, mem)

        self.t_next += self.period_sec
        if not self.done:
            threading.Timer(self.t_next - t_now, self._timeout).start()
