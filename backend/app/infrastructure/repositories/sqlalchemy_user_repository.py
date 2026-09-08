import uuid

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.domain.entities.user import User
from app.domain.repositories.user_repository import UserRepository
from app.infrastructure.db.models.user_model import UserModel


class SqlAlchemyUserRepository(UserRepository):
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def get_by_id(self, user_id: uuid.UUID) -> User | None:
        stmt = select(UserModel).options(selectinload(UserModel.role)).where(UserModel.id == user_id)
        model = (await self._session.execute(stmt)).scalar_one_or_none()
        return _to_entity(model) if model else None

    async def get_by_email(self, email: str) -> User | None:
        stmt = select(UserModel).options(selectinload(UserModel.role)).where(UserModel.email == email)
        model = (await self._session.execute(stmt)).scalar_one_or_none()
        return _to_entity(model) if model else None

    async def list(self, *, page: int, page_size: int) -> tuple[list[User], int]:
        total = (await self._session.execute(select(func.count()).select_from(UserModel))).scalar_one()

        stmt = (
            select(UserModel)
            .options(selectinload(UserModel.role))
            .order_by(UserModel.created_at.desc())
            .offset((page - 1) * page_size)
            .limit(page_size)
        )
        models = (await self._session.execute(stmt)).scalars().all()
        return [_to_entity(model) for model in models], total

    async def create(self, user: User) -> User:
        model = UserModel(
            email=user.email,
            hashed_password=user.hashed_password,
            full_name=user.full_name,
            role_id=user.role_id,
            is_active=user.is_active,
        )
        self._session.add(model)
        await self._session.flush()
        await self._session.refresh(model, attribute_names=["role"])
        return _to_entity(model)

    async def update(self, user: User) -> User:
        model = await self._session.get(UserModel, user.id, options=[selectinload(UserModel.role)])
        if model is None:
            raise ValueError(f"User {user.id} does not exist")
        model.full_name = user.full_name
        model.is_active = user.is_active
        model.role_id = user.role_id
        await self._session.flush()
        return _to_entity(model)

    async def delete(self, user_id: uuid.UUID) -> None:
        model = await self._session.get(UserModel, user_id)
        if model is not None:
            await self._session.delete(model)
            await self._session.flush()


def _to_entity(model: UserModel) -> User:
    return User(
        id=model.id,
        email=model.email,
        hashed_password=model.hashed_password,
        full_name=model.full_name,
        role_id=model.role_id,
        role_name=model.role.name if model.role else "",
        is_active=model.is_active,
        created_at=model.created_at,
        updated_at=model.updated_at,
    )
