import enum


class Status(enum.Enum):
    NOT_STARTED = 1
    RUNNING = 2
    COMPLETED = 3
    FAILED = 4
    CANCELLED = 5
    PARENT_FAILED = 6

    def __str__(self):
        return self.name.replace("_", " ").title()
