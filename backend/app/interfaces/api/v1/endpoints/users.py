import uuid
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Security, status

from app.domain.entities.user import RoleName, User
from app.domain.repositories.user_repository import UserRepository
from app.interfaces.api.v1.deps import get_current_active_user, get_user_repository
from app.interfaces.api.v1.schemas.common import PaginatedResponse
from app.interfaces.api.v1.schemas.user_schemas import UserResponse

router = APIRouter(prefix="/users", tags=["users"])

_READ_ROLES = [RoleName.ADMIN.value, RoleName.MANAGER.value]


def _to_response(user: User) -> UserResponse:
    return UserResponse(id=user.id, email=user.email, full_name=user.full_name, role=user.role_name, is_active=user.is_active)


@router.get("", response_model=PaginatedResponse[UserResponse])
async def list_users(
    user_repo: Annotated[UserRepository, Depends(get_user_repository)],
    _current_user: Annotated[User, Security(get_current_active_user, scopes=_READ_ROLES)],
    page: int = 1,
    page_size: int = 20,
) -> PaginatedResponse[UserResponse]:
    users, total = await user_repo.list(page=page, page_size=page_size)
    return PaginatedResponse(items=[_to_response(u) for u in users], total=total, page=page, page_size=page_size)


@router.get("/{user_id}", response_model=UserResponse)
async def get_user(
    user_id: uuid.UUID,
    user_repo: Annotated[UserRepository, Depends(get_user_repository)],
    _current_user: Annotated[User, Security(get_current_active_user, scopes=_READ_ROLES)],
) -> UserResponse:
    user = await user_repo.get_by_id(user_id)
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return _to_response(user)
