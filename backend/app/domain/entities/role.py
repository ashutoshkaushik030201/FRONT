from __future__ import annotations

from dataclasses import dataclass, field
from uuid import UUID


@dataclass
class Role:
    id: UUID | None
    name: str
    permissions: dict = field(default_factory=dict)
