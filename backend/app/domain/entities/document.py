from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from enum import Enum
from uuid import UUID


class DocumentType(str, Enum):
    MANUAL = "manual"
    CERTIFICATE = "certificate"


@dataclass
class Document:
    id: UUID | None
    asset_id: UUID
    doc_type: DocumentType
    file_name: str
    storage_path: str
    file_size_bytes: int
    uploaded_by: UUID | None = None
    created_at: datetime | None = None
