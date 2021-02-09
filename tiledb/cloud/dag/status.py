from enum import Enum


class Status(Enum):
    NOT_STARTED = "Not Started"
    RUNNING = "Running"
    COMPLETED = "Completed"
    FAILED = "Failed"
    CANCELLED = "Cancelled"
