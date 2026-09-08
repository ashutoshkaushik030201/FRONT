from __future__ import annotations

from datetime import date
from decimal import Decimal
from enum import Enum

_CENTS = Decimal("0.01")


class DepreciationMethod(str, Enum):
    STRAIGHT_LINE = "straight_line"
    DECLINING_BALANCE = "declining_balance"


def calculate_straight_line_monthly_depreciation(
    purchase_cost: Decimal, salvage_value: Decimal, useful_life_months: int
) -> Decimal:
    """Spreads the depreciable base evenly across the asset's useful life."""
    if useful_life_months <= 0:
        raise ValueError("useful_life_months must be positive")
    depreciable_base = purchase_cost - salvage_value
    if depreciable_base <= 0:
        return Decimal("0.00")
    return (depreciable_base / useful_life_months).quantize(_CENTS)


def calculate_declining_balance_monthly_depreciation(
    opening_book_value: Decimal, salvage_value: Decimal, annual_rate: Decimal
) -> Decimal:
    """Applies a fixed percentage rate to the current book value each period."""
    if opening_book_value <= salvage_value:
        return Decimal("0.00")
    monthly_rate = annual_rate / Decimal("12")
    max_allowed = opening_book_value - salvage_value
    amount = max_allowed * monthly_rate
    return min(amount, max_allowed).quantize(_CENTS)


def months_between(start: date, end: date) -> int:
    return (end.year - start.year) * 12 + (end.month - start.month)
