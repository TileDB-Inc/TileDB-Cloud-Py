import enum


class Mode(enum.Enum):
    """Mode to run a DAG in"""

    LOCAL = enum.auto()
    """Run on local machine (testing purposes)"""

    REALTIME = enum.auto()
    """Designed to return results directly to the client (default).
    Realtime task graphs are scheduled and executed immediately
    and are well suited for fast distributed workloads.
    """

    BATCH = enum.auto()
    """
    Designed for large, resource intensive asynchronous workloads.
    Batch task graphs are defined, uploaded, and scheduled for execution
    and are well suited for ingestion-style workloads.
    """

    def __str__(self):
        return self.name.replace("_", " ").title()
