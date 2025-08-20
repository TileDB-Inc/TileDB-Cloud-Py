"""Configuration classes for DAG decorators."""

import enum
from dataclasses import dataclass
from typing import Optional

from tiledb.cloud.dag import Mode
from tiledb.cloud.dag.decorators._resources import Resources
from tiledb.cloud.utilities.logging import get_logger

logger = get_logger()


@dataclass(frozen=False)
class BaseInput:
    """Base input class with common parameters for UDF and TaskGraph."""

    name: Optional[str] = None
    mode: enum.Enum = Mode.REALTIME
    namespace: Optional[str] = None
    retry_limit: int = 0
    timeout: Optional[int] = None
    wait: bool = True

    def sub_private(self, **kwargs):
        for k in kwargs:
            if k.startswith("_"):
                if k[1:] in self.__dict__:
                    logger.info(f"{k} detected. Override {k[1:]} with {kwargs[k]}")
                    setattr(self, k[1:], kwargs[k])

            # only relevant in UDFInput subclass
            if k in ["_resource_class", "_cpu", "_memory_gb"]:
                try:
                    setattr(self.resources, k[1:], kwargs[k])
                except AttributeError:
                    logger.debug(
                        "Resources object not found due to wrongly included in"
                        f" task graph. Skipping {k}."
                    )


@dataclass(frozen=False)
class UDFInput(BaseInput):
    """Input configuration for UDF decorator execution."""

    acn: Optional[str] = None
    resources: Optional[Resources] = None
    expand: Optional[str] = None
    image_name: Optional[str] = None


@dataclass(frozen=False)
class TaskGraphInput(BaseInput):
    """Input configuration for TaskGraph decorator execution."""

    max_workers: Optional[int] = None
    return_dag: bool = False
