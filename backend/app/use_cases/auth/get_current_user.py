import uuid

from app.domain.entities.user import User
from app.domain.exceptions import AuthenticationError
from app.domain.repositories.user_repository import UserRepository


class GetCurrentUserUseCase:
    """Resolves the authenticated user from a validated JWT subject claim."""

    def __init__(self, user_repository: UserRepository) -> None:
        self._user_repository = user_repository

    async def execute(self, user_id: str) -> User:
        try:
            parsed_id = uuid.UUID(user_id)
        except ValueError as exc:
            raise AuthenticationError("Invalid authentication token") from exc

        user = await self._user_repository.get_by_id(parsed_id)
        if user is None or not user.is_active:
            raise AuthenticationError("User not found or inactive")
        return user
