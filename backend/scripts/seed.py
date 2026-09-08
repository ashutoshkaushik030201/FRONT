"""Idempotent seed script: default roles, an admin/manager/viewer user, categories, sample assets."""
import asyncio
from datetime import date, datetime, timedelta, timezone
from decimal import Decimal

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.security import hash_password
from app.infrastructure.db.models.asset_assignment_model import AssetAssignmentModel
from app.infrastructure.db.models.asset_category_model import AssetCategoryModel
from app.infrastructure.db.models.asset_model import AssetModel
from app.infrastructure.db.models.role_model import RoleModel
from app.infrastructure.db.models.user_model import UserModel
from app.infrastructure.db.session import AsyncSessionLocal

_ROLES = [
    ("admin", {"full_access": True}),
    ("manager", {"manage_assets": True}),
    ("viewer", {"read_only": True}),
]

_CATEGORIES = [
    ("Laptops", "hardware"),
    ("Servers", "hardware"),
    ("Productivity Software", "software_license"),
]

_DEFAULT_PASSWORD = "ChangeMe123!"


async def _get_or_create_role(session: AsyncSession, name: str, permissions: dict) -> RoleModel:
    role = (await session.execute(select(RoleModel).where(RoleModel.name == name))).scalar_one_or_none()
    if role is None:
        role = RoleModel(name=name, permissions=permissions)
        session.add(role)
        await session.flush()
    return role


async def _get_or_create_category(session: AsyncSession, name: str, type_: str) -> AssetCategoryModel:
    category = (
        await session.execute(select(AssetCategoryModel).where(AssetCategoryModel.name == name))
    ).scalar_one_or_none()
    if category is None:
        category = AssetCategoryModel(name=name, type=type_)
        session.add(category)
        await session.flush()
    return category


async def _get_or_create_user(
    session: AsyncSession, email: str, full_name: str, role: RoleModel, password: str
) -> UserModel:
    user = (await session.execute(select(UserModel).where(UserModel.email == email))).scalar_one_or_none()
    if user is None:
        user = UserModel(
            email=email,
            hashed_password=hash_password(password),
            full_name=full_name,
            role_id=role.id,
            is_active=True,
        )
        session.add(user)
        await session.flush()
    return user


async def _get_or_create_asset(session: AsyncSession, category: AssetCategoryModel, **kwargs) -> AssetModel:
    asset = (
        await session.execute(select(AssetModel).where(AssetModel.asset_tag == kwargs["asset_tag"]))
    ).scalar_one_or_none()
    if asset is None:
        asset = AssetModel(category_id=category.id, **kwargs)
        session.add(asset)
        await session.flush()
    return asset


async def seed() -> None:
    async with AsyncSessionLocal() as session:
        roles = {name: await _get_or_create_role(session, name, perms) for name, perms in _ROLES}

        admin_user = await _get_or_create_user(
            session, "admin@nexus.io", "Nexus Administrator", roles["admin"], _DEFAULT_PASSWORD
        )
        manager_user = await _get_or_create_user(
            session, "manager@nexus.io", "Asset Manager", roles["manager"], _DEFAULT_PASSWORD
        )
        await _get_or_create_user(session, "viewer@nexus.io", "Read Only Viewer", roles["viewer"], _DEFAULT_PASSWORD)

        categories = {name: await _get_or_create_category(session, name, type_) for name, type_ in _CATEGORIES}

        today = date.today()
        laptop = await _get_or_create_asset(
            session,
            categories["Laptops"],
            asset_tag="HW-LAPTOP-0001",
            name="Dell Latitude 5540",
            description="Standard-issue engineering laptop",
            status="active",
            purchase_cost=Decimal("1450.00"),
            purchase_date=today - timedelta(days=400),
            salvage_value=Decimal("150.00"),
            useful_life_months=36,
            depreciation_method="straight_line",
            asset_metadata={"serial_no": "SN-0001", "vendor": "Dell"},
            assigned_to_user_id=manager_user.id,
        )
        await _get_or_create_asset(
            session,
            categories["Servers"],
            asset_tag="HW-SERVER-0001",
            name="Dell PowerEdge R750",
            description="Primary application server",
            status="active",
            purchase_cost=Decimal("8200.00"),
            purchase_date=today - timedelta(days=900),
            salvage_value=Decimal("500.00"),
            useful_life_months=60,
            depreciation_method="declining_balance",
            asset_metadata={"serial_no": "SN-1001", "vendor": "Dell"},
        )
        await _get_or_create_asset(
            session,
            categories["Productivity Software"],
            asset_tag="SW-M365-0001",
            name="Microsoft 365 E5 License",
            description="Enterprise productivity suite license",
            status="active",
            purchase_cost=Decimal("2400.00"),
            purchase_date=today - timedelta(days=200),
            salvage_value=Decimal("0.00"),
            useful_life_months=12,
            depreciation_method="straight_line",
            asset_metadata={"license_key": "XXXXX-XXXXX-XXXXX", "seats": 50},
        )

        has_history = (
            await session.execute(select(AssetAssignmentModel).where(AssetAssignmentModel.asset_id == laptop.id))
        ).scalar_one_or_none()
        if has_history is None:
            session.add(
                AssetAssignmentModel(
                    asset_id=laptop.id,
                    user_id=manager_user.id,
                    assigned_at=datetime.now(timezone.utc) - timedelta(days=400),
                    notes="Initial assignment at onboarding",
                )
            )

        await session.commit()

        print("Seed data created/verified successfully.")
        print(f"  Admin login:   admin@nexus.io / {_DEFAULT_PASSWORD}")
        print(f"  Manager login: manager@nexus.io / {_DEFAULT_PASSWORD}")
        print(f"  Viewer login:  viewer@nexus.io / {_DEFAULT_PASSWORD}")


if __name__ == "__main__":
    asyncio.run(seed())
