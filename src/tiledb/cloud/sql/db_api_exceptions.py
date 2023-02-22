class Error(Exception):
    """Base class for exceptions in the DB API 2.0 implementation."""


class InterfaceError(Error):
    """Raised when the database encountered a programming error."""


class DatabaseError(Error):
    """Raised when the database encountered a programming error."""


class Warning(Exception):
    """Exception for important warnings."""


class ProgrammingError(Error):
    """Raised when the database encountered a programming error."""


class DataError(Error):
    """Raised when the database encountered data-related errors."""


class OperationalError(Error):
    """Raised when the database encountered operational errors."""


class IntegrityError(Error):
    """Raised when the database encountered an integrity constraint error."""


class InternalError(Error):
    """Raised when the database encountered an internal error."""


class NotSupportedError(Error):
    """Raised when the database encountered a feature not supported error."""
