from abc import ABC, abstractmethod
from uuid import UUID

from app.domain.entities.role import Role


class RoleRepository(ABC):
    """Port defining read access to roles used for RBAC and user provisioning."""

    @abstractmethod
    async def get_by_name(self, name: str) -> Role | None: ...

    @abstractmethod
    async def get_by_id(self, role_id: UUID) -> Role | None: ...

    @abstractmethod
    async def list(self) -> list[Role]: ...
