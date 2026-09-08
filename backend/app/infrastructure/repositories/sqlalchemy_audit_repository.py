import uuid

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.entities.audit_log import AuditAction, AuditLog
from app.domain.repositories.audit_repository import AuditRepository
from app.infrastructure.db.models.audit_log_model import AuditLogModel


class SqlAlchemyAuditRepository(AuditRepository):
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def create(self, audit_log: AuditLog) -> AuditLog:
        model = AuditLogModel(
            user_id=audit_log.user_id,
            action=audit_log.action.value,
            entity_type=audit_log.entity_type,
            entity_id=audit_log.entity_id,
            old_values=audit_log.old_values,
            new_values=audit_log.new_values,
            ip_address=audit_log.ip_address,
        )
        self._session.add(model)
        await self._session.flush()
        await self._session.refresh(model)
        return _to_entity(model)

    async def list(
        self,
        *,
        page: int,
        page_size: int,
        entity_type: str | None = None,
        entity_id: uuid.UUID | None = None,
        user_id: uuid.UUID | None = None,
    ) -> tuple[list[AuditLog], int]:
        conditions = []
        if entity_type is not None:
            conditions.append(AuditLogModel.entity_type == entity_type)
        if entity_id is not None:
            conditions.append(AuditLogModel.entity_id == entity_id)
        if user_id is not None:
            conditions.append(AuditLogModel.user_id == user_id)

        total = (
            await self._session.execute(select(func.count()).select_from(AuditLogModel).where(*conditions))
        ).scalar_one()

        stmt = (
            select(AuditLogModel)
            .where(*conditions)
            .order_by(AuditLogModel.created_at.desc())
            .offset((page - 1) * page_size)
            .limit(page_size)
        )
        models = (await self._session.execute(stmt)).scalars().all()
        return [_to_entity(model) for model in models], total


def _to_entity(model: AuditLogModel) -> AuditLog:
    return AuditLog(
        id=model.id,
        action=AuditAction(model.action),
        entity_type=model.entity_type,
        entity_id=model.entity_id,
        user_id=model.user_id,
        old_values=model.old_values,
        new_values=model.new_values,
        ip_address=model.ip_address,
        created_at=model.created_at,
    )
