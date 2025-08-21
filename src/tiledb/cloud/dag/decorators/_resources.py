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
    """Load default resources from toml file."""

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
    resource_opts: Sequence[str] = field(
        default_factory=lambda: load_defaults(
            file="resources.toml",
            toml_key="resource_options",
        )
    )
    """Valid resource classes."""

    def translate_to_resource_class(self) -> None:
        """Translate as best as possible from custom resources to
        resource class.

        standard - 2 cpu, 2Gi memory
        large - 8 cpu, 8Gi memory

        :return: Resource class.
        """

        if self.cpu <= 2 and self.memory_gb <= 2:
            self.resource_class = "standard"
        else:
            self.resource_class = "large"

    def translate_to_cpu_memory_gb(self) -> None:
        """Translate resource class to cpu + memory_gb."""

        if self.resource_class == "standard":
            self.cpu = 2
            self.memory_gb = 2
        elif self.resource_class == "large":
            self.cpu = 8
            self.memory_gb = 8

    def _set_defaults(self, mode: enum.Enum) -> None:
        """Set default resources based on mode."""

        if mode == Mode.REALTIME:
            logger.debug("Using default resource class.")
            self.resource_class = self.resource_opts[0]
        elif mode == Mode.BATCH:
            logger.debug("Using default cpu + memory_gb.")
            self.cpu = 2
            self.memory_gb = 2

    def _validate_and_translate(self, mode: enum.Enum) -> None:
        """Validate existing resources and translate if needed."""

        if mode == Mode.REALTIME:
            if self.resource_class:
                self._validate_resource_class()
            else:
                logger.debug("Translating cpu + memory_gb to resource class.")
                self.translate_to_resource_class()
        elif mode == Mode.BATCH:
            if self.cpu or self.memory_gb:
                self.cpu = self.cpu or 2
                self.memory_gb = self.memory_gb or 2
            else:
                logger.debug("Translating resource class to cpu + memory_gb.")
                self.translate_to_cpu_memory_gb()

    def _validate_resource_class(self) -> None:
        """Validate resource class is in allowed options."""

        self.resource_class = self.resource_class.lower()
        if self.resource_class not in self.resource_opts:
            logger.warning(
                f"Invalid resource class: {self.resource_class}. "
                f"Must be one of {self.resource_opts}. "
                f"Forcing default resource class."
            )
            self._set_defaults(Mode.REALTIME)

    def validate(self, mode: enum.Enum) -> None:
        """Validate resources based on input and mode requirements."""

        if mode == Mode.LOCAL:
            return None

        has_resources = any([self.cpu, self.memory_gb, self.resource_class])

        if not has_resources:
            self._set_defaults(mode)
        else:
            self._validate_and_translate(mode)
