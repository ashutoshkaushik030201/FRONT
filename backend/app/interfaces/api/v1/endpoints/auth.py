from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Security, status
from fastapi.security import OAuth2PasswordRequestForm

from app.domain.entities.user import RoleName
from app.domain.exceptions import AuthenticationError, DuplicateEntityError, EntityNotFoundError
from app.interfaces.api.v1.deps import CurrentUser, get_current_active_user, get_login_use_case, get_register_use_case
from app.interfaces.api.v1.schemas.auth_schemas import RegisterRequest, TokenResponse
from app.interfaces.api.v1.schemas.user_schemas import UserResponse
from app.use_cases.auth.login import LoginUseCase
from app.use_cases.auth.register import RegisterUseCase, RegisterUserInput

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def register(
    payload: RegisterRequest,
    use_case: Annotated[RegisterUseCase, Depends(get_register_use_case)],
    _current_user: Annotated[object, Security(get_current_active_user, scopes=[RoleName.ADMIN.value])],
) -> UserResponse:
    try:
        user = await use_case.execute(
            RegisterUserInput(
                email=payload.email,
                password=payload.password,
                full_name=payload.full_name,
                role_name=payload.role.value,
            )
        )
    except DuplicateEntityError as exc:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(exc)) from exc
    except EntityNotFoundError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc

    return UserResponse(id=user.id, email=user.email, full_name=user.full_name, role=user.role_name, is_active=user.is_active)


@router.post("/login", response_model=TokenResponse)
async def login(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    use_case: Annotated[LoginUseCase, Depends(get_login_use_case)],
) -> TokenResponse:
    try:
        result = await use_case.execute(form_data.username, form_data.password)
    except AuthenticationError as exc:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=str(exc),
            headers={"WWW-Authenticate": "Bearer"},
        ) from exc

    return TokenResponse(access_token=result.access_token, refresh_token=result.refresh_token)


@router.get("/me", response_model=UserResponse)
async def read_current_user(current_user: CurrentUser) -> UserResponse:
    return UserResponse(
        id=current_user.id,
        email=current_user.email,
        full_name=current_user.full_name,
        role=current_user.role_name,
        is_active=current_user.is_active,
    )
