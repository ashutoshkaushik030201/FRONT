from __future__ import annotations

from dataclasses import dataclass
from uuid import UUID


@dataclass
class AssetCategory:
    id: UUID | None
    name: str
    type: str
