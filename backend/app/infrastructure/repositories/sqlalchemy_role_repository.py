import uuid

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.entities.role import Role
from app.domain.repositories.role_repository import RoleRepository
from app.infrastructure.db.models.role_model import RoleModel


class SqlAlchemyRoleRepository(RoleRepository):
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def get_by_name(self, name: str) -> Role | None:
        stmt = select(RoleModel).where(RoleModel.name == name)
        model = (await self._session.execute(stmt)).scalar_one_or_none()
        return _to_entity(model) if model else None

    async def get_by_id(self, role_id: uuid.UUID) -> Role | None:
        model = await self._session.get(RoleModel, role_id)
        return _to_entity(model) if model else None

    async def list(self) -> list[Role]:
        models = (await self._session.execute(select(RoleModel))).scalars().all()
        return [_to_entity(model) for model in models]


def _to_entity(model: RoleModel) -> Role:
    return Role(id=model.id, name=model.name, permissions=model.permissions)
