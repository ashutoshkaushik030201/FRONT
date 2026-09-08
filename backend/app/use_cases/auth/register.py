from dataclasses import dataclass

from app.core.security import hash_password
from app.domain.entities.user import User
from app.domain.exceptions import DuplicateEntityError, EntityNotFoundError
from app.domain.repositories.role_repository import RoleRepository
from app.domain.repositories.user_repository import UserRepository


@dataclass
class RegisterUserInput:
    email: str
    password: str
    full_name: str
    role_name: str


class RegisterUseCase:
    def __init__(self, user_repository: UserRepository, role_repository: RoleRepository) -> None:
        self._user_repository = user_repository
        self._role_repository = role_repository

    async def execute(self, data: RegisterUserInput) -> User:
        existing = await self._user_repository.get_by_email(data.email)
        if existing is not None:
            raise DuplicateEntityError("User", "email", data.email)

        role = await self._role_repository.get_by_name(data.role_name)
        if role is None or role.id is None:
            raise EntityNotFoundError("Role", data.role_name)

        user = User(
            id=None,
            email=data.email,
            hashed_password=hash_password(data.password),
            full_name=data.full_name,
            role_id=role.id,
            role_name=role.name,
        )
        return await self._user_repository.create(user)
