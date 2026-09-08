"""Imports every ORM model so Base.metadata is fully populated for Alembic autogenerate."""
from app.infrastructure.db.models.asset_assignment_model import AssetAssignmentModel
from app.infrastructure.db.models.asset_category_model import AssetCategoryModel
from app.infrastructure.db.models.asset_model import AssetModel
from app.infrastructure.db.models.audit_log_model import AuditLogModel
from app.infrastructure.db.models.depreciation_schedule_model import DepreciationScheduleModel
from app.infrastructure.db.models.document_model import DocumentModel
from app.infrastructure.db.models.role_model import RoleModel
from app.infrastructure.db.models.user_model import UserModel

__all__ = [
    "AssetAssignmentModel",
    "AssetCategoryModel",
    "AssetModel",
    "AuditLogModel",
    "DepreciationScheduleModel",
    "DocumentModel",
    "RoleModel",
    "UserModel",
]
