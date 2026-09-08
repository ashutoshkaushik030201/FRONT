class AppException(Exception):
    """Base class for exceptions that should be translated into HTTP responses."""

    status_code: int = 500
    error_code: str = "internal_error"

    def __init__(self, message: str, *, details: dict | None = None) -> None:
        super().__init__(message)
        self.message = message
        self.details = details or {}


class NotFoundException(AppException):
    status_code = 404
    error_code = "not_found"


class ConflictException(AppException):
    status_code = 409
    error_code = "conflict"


class UnauthorizedException(AppException):
    status_code = 401
    error_code = "unauthorized"


class ForbiddenException(AppException):
    status_code = 403
    error_code = "forbidden"


class ValidationException(AppException):
    status_code = 422
    error_code = "validation_error"
