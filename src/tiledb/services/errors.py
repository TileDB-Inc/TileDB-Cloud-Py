from tiledb import TileDBError


class TileDBCloudError(TileDBError):
    """Generic base TileDB Cloud API exception class."""

    code = 500

    def __init__(self, message=None, code=None) -> None:
        super().__init__()

        if code:
            self.code = code
        self.message = message or "Internal Server Error"

    def __str__(self):
        return f"[{self.message}] - Code: {self.code}"


class BadRequest(TileDBCloudError):
    """Custom Exception to be raised if a request sends wrong or malformed payload."""

    code = 400


class Unauthorized(TileDBCloudError):
    """Custom Exception to be raised if a request user is not authenticated."""

    code = 401


class NotFound(TileDBCloudError):
    """Custom Exception to be raised if a resource was not found."""

    code = 404


class MethodNotAllowed(TileDBCloudError):
    """
    Custom Exception to be raised if a request method
    is not allowed by the endpoint service.
    """

    code = 405


class ResourceConflict(TileDBCloudError):
    """Custom Exception to be raised if a resource's state is not the expected."""

    code = 409


class Unavailable(TileDBCloudError):
    """Custom Exception to be raised if a service was unavailable."""

    pass
