"""Composition point for the interface layer: repository/use-case providers and RBAC guards."""
from typing import Annotated

from fastapi import Depends, HTTPException, Security, status
from fastapi.security import OAuth2PasswordBearer, SecurityScopes
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.security import decode_token
from app.domain.entities.user import RoleName, User
from app.domain.exceptions import AuthenticationError
from app.domain.repositories.asset_assignment_repository import AssetAssignmentRepository
from app.domain.repositories.asset_category_repository import AssetCategoryRepository
from app.domain.repositories.asset_repository import AssetRepository
from app.domain.repositories.audit_repository import AuditRepository
from app.domain.repositories.depreciation_schedule_repository import DepreciationScheduleRepository
from app.domain.repositories.role_repository import RoleRepository
from app.domain.repositories.user_repository import UserRepository
from app.infrastructure.db.session import get_db
from app.infrastructure.di.container import (
    build_asset_assignment_repository,
    build_asset_category_repository,
    build_asset_repository,
    build_audit_repository,
    build_depreciation_schedule_repository,
    build_role_repository,
    build_user_repository,
)
from app.use_cases.asset.assign_asset import AssignAssetUseCase
from app.use_cases.asset.calculate_depreciation import CalculateDepreciationUseCase
from app.use_cases.asset.create_asset import CreateAssetUseCase
from app.use_cases.asset.list_assets import ListAssetsUseCase
from app.use_cases.asset.update_asset import UpdateAssetUseCase
from app.use_cases.auth.get_current_user import GetCurrentUserUseCase
from app.use_cases.auth.login import LoginUseCase
from app.use_cases.auth.register import RegisterUseCase

oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="/api/v1/auth/login",
    scopes={role.value: f"{role.value.capitalize()} access" for role in RoleName},
)

DbSession = Annotated[AsyncSession, Depends(get_db)]


# ---- repository providers (infra adapters wired to domain ports) ----


def get_asset_repository(session: DbSession) -> AssetRepository:
    return build_asset_repository(session)


def get_asset_category_repository(session: DbSession) -> AssetCategoryRepository:
    return build_asset_category_repository(session)


def get_user_repository(session: DbSession) -> UserRepository:
    return build_user_repository(session)


def get_role_repository(session: DbSession) -> RoleRepository:
    return build_role_repository(session)


def get_audit_repository(session: DbSession) -> AuditRepository:
    return build_audit_repository(session)


def get_asset_assignment_repository(session: DbSession) -> AssetAssignmentRepository:
    return build_asset_assignment_repository(session)


def get_depreciation_schedule_repository(session: DbSession) -> DepreciationScheduleRepository:
    return build_depreciation_schedule_repository(session)


# ---- use case providers ----


def get_login_use_case(user_repo: Annotated[UserRepository, Depends(get_user_repository)]) -> LoginUseCase:
    return LoginUseCase(user_repo)


def get_register_use_case(
    user_repo: Annotated[UserRepository, Depends(get_user_repository)],
    role_repo: Annotated[RoleRepository, Depends(get_role_repository)],
) -> RegisterUseCase:
    return RegisterUseCase(user_repo, role_repo)


def get_current_user_use_case(
    user_repo: Annotated[UserRepository, Depends(get_user_repository)],
) -> GetCurrentUserUseCase:
    return GetCurrentUserUseCase(user_repo)


def get_create_asset_use_case(
    asset_repo: Annotated[AssetRepository, Depends(get_asset_repository)],
) -> CreateAssetUseCase:
    return CreateAssetUseCase(asset_repo)


def get_update_asset_use_case(
    asset_repo: Annotated[AssetRepository, Depends(get_asset_repository)],
) -> UpdateAssetUseCase:
    return UpdateAssetUseCase(asset_repo)


def get_list_assets_use_case(
    asset_repo: Annotated[AssetRepository, Depends(get_asset_repository)],
) -> ListAssetsUseCase:
    return ListAssetsUseCase(asset_repo)


def get_calculate_depreciation_use_case(
    asset_repo: Annotated[AssetRepository, Depends(get_asset_repository)],
    schedule_repo: Annotated[DepreciationScheduleRepository, Depends(get_depreciation_schedule_repository)],
) -> CalculateDepreciationUseCase:
    return CalculateDepreciationUseCase(asset_repo, schedule_repo)


def get_assign_asset_use_case(
    asset_repo: Annotated[AssetRepository, Depends(get_asset_repository)],
    user_repo: Annotated[UserRepository, Depends(get_user_repository)],
    assignment_repo: Annotated[AssetAssignmentRepository, Depends(get_asset_assignment_repository)],
) -> AssignAssetUseCase:
    return AssignAssetUseCase(asset_repo, user_repo, assignment_repo)


# ---- authentication / RBAC ----


async def get_current_active_user(
    security_scopes: SecurityScopes,
    token: Annotated[str, Depends(oauth2_scheme)],
    use_case: Annotated[GetCurrentUserUseCase, Depends(get_current_user_use_case)],
) -> User:
    """Validates the bearer token and enforces that the user's role is in `security_scopes`.

    Usage: `Security(get_current_active_user, scopes=["admin"])`. An empty scopes list only
    requires a valid, active user regardless of role. The "admin" role always passes.
    """
    authenticate_value = f'Bearer scope="{security_scopes.scope_str}"' if security_scopes.scopes else "Bearer"
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": authenticate_value},
    )

    try:
        payload = decode_token(token)
    except ValueError as exc:
        raise credentials_exception from exc

    user_id = payload.get("sub")
    if user_id is None:
        raise credentials_exception

    try:
        user = await use_case.execute(user_id)
    except AuthenticationError as exc:
        raise credentials_exception from exc

    if security_scopes.scopes and user.role_name not in security_scopes.scopes and user.role_name != RoleName.ADMIN.value:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions",
            headers={"WWW-Authenticate": authenticate_value},
        )

    return user


CurrentUser = Annotated[User, Security(get_current_active_user)]
