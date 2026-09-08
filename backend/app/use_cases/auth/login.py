from dataclasses import dataclass

from app.core.security import create_access_token, create_refresh_token, verify_password
from app.domain.exceptions import AuthenticationError
from app.domain.repositories.user_repository import UserRepository


@dataclass
class LoginResult:
    access_token: str
    refresh_token: str
    token_type: str = "bearer"


class LoginUseCase:
    def __init__(self, user_repository: UserRepository) -> None:
        self._user_repository = user_repository

    async def execute(self, email: str, password: str) -> LoginResult:
        user = await self._user_repository.get_by_email(email)
        if user is None or not verify_password(password, user.hashed_password):
            raise AuthenticationError("Invalid email or password")
        if not user.is_active:
            raise AuthenticationError("User account is inactive")

        access_token = create_access_token(subject=str(user.id), extra_claims={"role": user.role_name})
        refresh_token = create_refresh_token(subject=str(user.id))
        return LoginResult(access_token=access_token, refresh_token=refresh_token)
