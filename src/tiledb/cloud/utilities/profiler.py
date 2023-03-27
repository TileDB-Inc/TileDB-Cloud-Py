import subprocess
import threading
import time
from typing import Optional

import numpy as np

import tiledb
from tiledb.cloud.utilities import max_memory_usage


def create_log_array(uri: str):
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

    a0 = tiledb.Attr(name="id", dtype="ascii", filters=ascii_fl)
    a1 = tiledb.Attr(name="op", dtype="ascii", filters=ascii_fl)
    a2 = tiledb.Attr(name="data", dtype="ascii", filters=ascii_fl)
    a3 = tiledb.Attr(name="extra", dtype="ascii", filters=ascii_fl)

    schema = tiledb.ArraySchema(
        domain=dom,
        sparse=True,
        attrs=[a0, a1, a2, a3],
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
):
    """
    Write an event to the log array.

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
    A simple profiler to log start/finish events with CPU and memory usage.
    """

    def __init__(
        self,
        uri: str,
        id: str,
        trace: bool = False,
    ):
        """
        Create a profiler object.

        :param uri: event log array URI
        :param id: profiler id, written to event id
        :param trace: enable trace logging, defaults to False
        """

        self.uri = uri
        self.id = id
        self.trace = trace
        self.array = tiledb.open(uri, "w")

        # Log node start time and system info
        node_id = open("/proc/sys/kernel/random/boot_id").read().strip()
        cmd = "uptime && free -h && uname -a && lscpu"
        node_info = self.run_cmd(cmd)
        self.write("start", node_id, node_info)

        # Start profiling timer
        self.done = False
        self.period_sec = 5
        self.t_start = time.time()
        self.t_next = self.t_start
        self.stats = ["time,cpu,mem"]
        self._timeout()

    def run_cmd(self, cmd: str) -> str:
        """
        Run a command and return the output.

        :param cmd: command to run
        :return: stdout from the command
        """

        res = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        if res.stderr:
            print(res.stderr)
        return res.stdout.strip()

    def write(self, op: str = "", data: str = "", extra: str = ""):
        """
        Write an event to the log array.

        :param op: event op, defaults to ""
        :param data: event data, defaults to ""
        :param extra: event extra data, defaults to ""
        """

        t_now_ms = time.time() * 1000

        if not self.uri:
            print(f"{t_now_ms},{self.id},{op},{data},{extra}")
            return

        self.array[t_now_ms] = {
            "id": [self.id],
            "op": [op],
            "data": [data],
            "extra": [extra],
        }

    def finish(self, extra: str = ""):
        """
        Write finish and stats events to the log array.

        :param extra: extra data for the finish event, defaults to ""
        """

        self.done = True
        t_elapsed = time.time() - self.t_start
        self.write("finish", f"{t_elapsed:.3f}", extra)
        mem = max_memory_usage()
        try:
            mem = (
                open("/sys/fs/cgroup/memory/memory.max_usage_in_bytes")
                .readline()
                .strip()
            )
        except Exception:
            # If we can't read the memory usage, set it to 0
            mem = "0"

        self.write("stats", mem, "\n".join(self.stats))

    def _timeout(self):
        """
        Capture system stats and schedule the next timeout.
        """

        try:
            cpu = open("/sys/fs/cgroup/cpu/cpuacct.usage").readline().strip()
            mem = open("/sys/fs/cgroup/memory/memory.usage_in_bytes").readline().strip()
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
