"""Handle resourcing for task graphs."""

import enum
from dataclasses import dataclass
from dataclasses import field
from typing import List, Optional, Sequence

import toml
from importlib_resources import files

from tiledb.cloud.dag import Mode
from tiledb.cloud.utilities.logging import get_logger

logger = get_logger()


def load_defaults(
    file: str,
    toml_key: str,
    config: str = "tiledb.cloud.dag.decorators.configs",
) -> List[str]:
    return toml.loads(files(config).joinpath(file).read_text())[toml_key]


@dataclass(frozen=False)
class Resources:
    """Resources container."""

    resource_class: Optional[str] = None
    """Realtime resource class."""
    cpu: Optional[int] = None
    """CPUs."""
    memory_gb: Optional[int] = None
    """Memory in GiB."""
    """Whether to validate resources on init. Rarely should be set to False."""
    resource_opts: Sequence[str] = field(
        default_factory=lambda: load_defaults(
            file="resources.toml",
            toml_key="resource_options",
        )
    )
    """Valid resource classes."""

    def translate_to_resource_class(self) -> str:
        """Translate as best as possible from custom resources to
        resource class.

        standard - 2 cpu, 2Gi memory
        large - 8 cpu, 8Gi memory

        :return: Resource class.
        """

        if self.cpu <= 2 and self.memory_gb <= 2:
            size = "standard"
        else:
            size = "large"

        logger.debug(f"Setting resource class to {size} based on cpu + memory_gb.")
        return size

    def validate(self, mode: enum.Enum) -> None:
        """Validate resources based on input and mode requirements."""

        if not self.cpu and not self.memory_gb and not self.resource_class:
            if mode == Mode.REALTIME:
                logger.debug(
                    "No REALTIME resources specified. Setting default resource class."
                )
                self.resource_class = self.resource_opts[0]
            elif mode == Mode.BATCH:
                logger.debug(
                    "No BATCH resources specified. Setting default cpu + memory_gb."
                )
                self.cpu = 2
                self.memory_gb = 2

        if self.resource_class:
            self.resource_class = self.resource_class.lower()

        # when one not set, force a default
        if self.cpu or self.memory_gb:
            self.cpu = self.cpu or 2
            self.memory_gb = self.memory_gb or 2

        if self.resource_class and self.resource_class not in self.resource_opts:
            raise ValueError(
                f"Invalid resource class: {self.resource_class}. "
                f"Must be one of {self.resource_opts}."
            )

        if self.resource_class and (self.cpu or self.memory_gb):
            raise ValueError("Cannot specify both resource_class and cpu + memory_gb.")

        if mode == Mode.REALTIME and (self.cpu or self.memory_gb):
            logger.debug("Translating cpu + memory_gb to resource class.")
            self.resource_class = self.translate_to_resource_class()
