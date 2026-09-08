class DomainError(Exception):
    """Base class for all domain-level errors, framework-agnostic."""


class EntityNotFoundError(DomainError):
    def __init__(self, entity_name: str, entity_id: object) -> None:
        super().__init__(f"{entity_name} with id '{entity_id}' was not found")
        self.entity_name = entity_name
        self.entity_id = entity_id


class DuplicateEntityError(DomainError):
    def __init__(self, entity_name: str, field_name: str, value: object) -> None:
        super().__init__(f"{entity_name} with {field_name}='{value}' already exists")
        self.entity_name = entity_name
        self.field_name = field_name
        self.value = value


class InvalidOperationError(DomainError):
    """Raised when an operation violates a business invariant."""


class AuthenticationError(DomainError):
    """Raised when credentials are missing, invalid, or expired."""


class AuthorizationError(DomainError):
    """Raised when an authenticated actor lacks permission for an operation."""
