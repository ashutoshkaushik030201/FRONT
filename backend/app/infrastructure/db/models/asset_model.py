import uuid
from datetime import date, datetime
from decimal import Decimal

from sqlalchemy import Computed, Date, DateTime, ForeignKey, Index, Numeric, String, Text
from sqlalchemy.dialects.postgresql import JSONB, TSVECTOR
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.infrastructure.db.base import Base, TimestampMixin


class AssetModel(Base, TimestampMixin):
    __tablename__ = "assets"
    __table_args__ = (
        Index("ix_assets_search_vector", "search_vector", postgresql_using="gin"),
        Index("ix_assets_metadata", "metadata", postgresql_using="gin"),
    )

    id: Mapped[uuid.UUID] = mapped_column(PG_UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    asset_tag: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    category_id: Mapped[uuid.UUID] = mapped_column(
        PG_UUID(as_uuid=True), ForeignKey("asset_categories.id"), nullable=False, index=True
    )
    status: Mapped[str] = mapped_column(String(20), nullable=False, default="active")
    assigned_to_user_id: Mapped[uuid.UUID | None] = mapped_column(
        PG_UUID(as_uuid=True), ForeignKey("users.id"), nullable=True, index=True
    )
    purchase_cost: Mapped[Decimal] = mapped_column(Numeric(12, 2), nullable=False)
    purchase_date: Mapped[date] = mapped_column(Date, nullable=False)
    salvage_value: Mapped[Decimal] = mapped_column(Numeric(12, 2), nullable=False, default=0)
    useful_life_months: Mapped[int] = mapped_column(nullable=False)
    depreciation_method: Mapped[str] = mapped_column(String(30), nullable=False, default="straight_line")
    asset_metadata: Mapped[dict] = mapped_column("metadata", JSONB, nullable=False, default=dict)
    deleted_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    search_vector: Mapped[str | None] = mapped_column(
        TSVECTOR,
        Computed(
            "to_tsvector('english', coalesce(name, '') || ' ' || coalesce(description, '') "
            "|| ' ' || coalesce(asset_tag, ''))",
            persisted=True,
        ),
        nullable=True,
    )

    category: Mapped["AssetCategoryModel"] = relationship(back_populates="assets")
    assigned_to: Mapped["UserModel | None"] = relationship(
        back_populates="assigned_assets", foreign_keys=[assigned_to_user_id]
    )
    assignments: Mapped[list["AssetAssignmentModel"]] = relationship(
        back_populates="asset", cascade="all, delete-orphan"
    )
    depreciation_schedules: Mapped[list["DepreciationScheduleModel"]] = relationship(
        back_populates="asset", cascade="all, delete-orphan"
    )
    documents: Mapped[list["DocumentModel"]] = relationship(
        back_populates="asset", cascade="all, delete-orphan"
    )
