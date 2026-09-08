import uuid
from dataclasses import dataclass
from datetime import date
from decimal import Decimal

from app.domain.entities.depreciation_schedule import DepreciationSchedule
from app.domain.exceptions import EntityNotFoundError
from app.domain.repositories.asset_repository import AssetRepository
from app.domain.repositories.depreciation_schedule_repository import DepreciationScheduleRepository
from app.domain.value_objects.depreciation_method import (
    DepreciationMethod,
    calculate_declining_balance_monthly_depreciation,
    calculate_straight_line_monthly_depreciation,
    months_between,
)

_DECLINING_BALANCE_ANNUAL_RATE = Decimal("0.20")


class CalculateDepreciationUseCase:
    """Recomputes and persists the full monthly depreciation schedule for an asset."""

    def __init__(
        self,
        asset_repository: AssetRepository,
        depreciation_schedule_repository: DepreciationScheduleRepository,
    ) -> None:
        self._asset_repository = asset_repository
        self._schedule_repository = depreciation_schedule_repository

    async def execute(self, asset_id: uuid.UUID, *, as_of: date | None = None) -> list[DepreciationSchedule]:
        asset = await self._asset_repository.get_by_id(asset_id)
        if asset is None or asset.is_deleted:
            raise EntityNotFoundError("Asset", asset_id)

        as_of = as_of or date.today()
        elapsed_months = max(0, min(asset.useful_life_months, months_between(asset.purchase_date, as_of)))

        schedules: list[DepreciationSchedule] = []
        opening_value = asset.purchase_cost
        period_cursor = asset.purchase_date

        for month_index in range(1, elapsed_months + 1):
            period_start = period_cursor
            period_end = _add_months(asset.purchase_date, month_index)

            if asset.depreciation_method == DepreciationMethod.STRAIGHT_LINE:
                amount = calculate_straight_line_monthly_depreciation(
                    asset.purchase_cost, asset.salvage_value, asset.useful_life_months
                )
            else:
                amount = calculate_declining_balance_monthly_depreciation(
                    opening_value, asset.salvage_value, _DECLINING_BALANCE_ANNUAL_RATE
                )

            closing_value = max(asset.salvage_value, opening_value - amount)

            schedules.append(
                DepreciationSchedule(
                    id=None,
                    asset_id=asset_id,
                    period_start=period_start,
                    period_end=period_end,
                    opening_book_value=opening_value,
                    depreciation_amount=amount,
                    closing_book_value=closing_value,
                )
            )

            opening_value = closing_value
            period_cursor = period_end

        return await self._schedule_repository.replace_for_asset(asset_id, schedules)


def _add_months(start: date, months: int) -> date:
    total_month_index = start.month - 1 + months
    year = start.year + total_month_index // 12
    month = total_month_index % 12 + 1
    day = min(start.day, _days_in_month(year, month))
    return date(year, month, day)


def _days_in_month(year: int, month: int) -> int:
    if month == 12:
        return (date(year + 1, 1, 1) - date(year, 12, 1)).days
    return (date(year, month + 1, 1) - date(year, month, 1)).days
