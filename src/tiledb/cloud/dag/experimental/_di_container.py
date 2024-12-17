"""Dependency injections container."""

from logging import Logger
from typing import Optional

from attrs import define
from pydantic import dataclasses as pydantic_dataclasses

from ...utilities import get_logger_wrapper
from ..dag import DAG
from ..dag import Mode


@pydantic_dataclasses.dataclass(frozen=False)
class UdfName:
    """Naming convention for UDFs."""

    name: Optional[str] = None
    """Name of the UDF."""
    mode: Mode = Mode.REALTIME
    """Mode of the graph orchestrating UDF."""

    def __post_init__(self) -> None:
        self.name = self.name or "UDF"

    @property
    def taskgraph(self) -> str:
        prefix = "realtime" if self.mode == Mode.REALTIME else "batch"
        return f"{prefix}->{self.name}"

    @property
    def task(self) -> str:
        return self.name


@define
class DIContainer:
    """Dependency injection container for DAG."""

    mode: Mode = Mode.REALTIME
    """DAG runtime mode."""

    def logger(self, level: int) -> Logger:
        return get_logger_wrapper(level=level)

    def graph(self, name: str, namespace: str) -> DAG:
        return DAG(
            name=name,
            namespace=namespace,
            mode=self.mode,
        )

    def name(self, name: str) -> UdfName:
        return UdfName(name, self.mode)
