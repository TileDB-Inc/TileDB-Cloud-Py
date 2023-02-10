import enum


class Mode(enum.Enum):
    """Mode to run in"""

    LOCAL = enum.auto()
    REALTIME = enum.auto()
    BATCH = enum.auto()

    def __str__(self):
        return self.name.replace("_", " ").title()
