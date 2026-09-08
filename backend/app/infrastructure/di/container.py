"""Wires concrete infrastructure adapters to the domain repository ports (composition root)."""
from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.repositories.asset_assignment_repository import AssetAssignmentRepository
from app.domain.repositories.asset_category_repository import AssetCategoryRepository
from app.domain.repositories.asset_repository import AssetRepository
from app.domain.repositories.audit_repository import AuditRepository
from app.domain.repositories.depreciation_schedule_repository import DepreciationScheduleRepository
from app.domain.repositories.role_repository import RoleRepository
from app.domain.repositories.user_repository import UserRepository
from app.infrastructure.repositories.sqlalchemy_asset_assignment_repository import (
    SqlAlchemyAssetAssignmentRepository,
)
from app.infrastructure.repositories.sqlalchemy_asset_category_repository import SqlAlchemyAssetCategoryRepository
from app.infrastructure.repositories.sqlalchemy_asset_repository import SqlAlchemyAssetRepository
from app.infrastructure.repositories.sqlalchemy_audit_repository import SqlAlchemyAuditRepository
from app.infrastructure.repositories.sqlalchemy_depreciation_schedule_repository import (
    SqlAlchemyDepreciationScheduleRepository,
)
from app.infrastructure.repositories.sqlalchemy_role_repository import SqlAlchemyRoleRepository
from app.infrastructure.repositories.sqlalchemy_user_repository import SqlAlchemyUserRepository


def build_asset_repository(session: AsyncSession) -> AssetRepository:
    return SqlAlchemyAssetRepository(session)


def build_asset_category_repository(session: AsyncSession) -> AssetCategoryRepository:
    return SqlAlchemyAssetCategoryRepository(session)


def build_user_repository(session: AsyncSession) -> UserRepository:
    return SqlAlchemyUserRepository(session)


def build_role_repository(session: AsyncSession) -> RoleRepository:
    return SqlAlchemyRoleRepository(session)


def build_audit_repository(session: AsyncSession) -> AuditRepository:
    return SqlAlchemyAuditRepository(session)


def build_asset_assignment_repository(session: AsyncSession) -> AssetAssignmentRepository:
    return SqlAlchemyAssetAssignmentRepository(session)


def build_depreciation_schedule_repository(session: AsyncSession) -> DepreciationScheduleRepository:
    return SqlAlchemyDepreciationScheduleRepository(session)
