"""Intercepts write requests (POST/PUT/PATCH/DELETE) and records them into audit_logs."""
import json
import re
import uuid
from collections.abc import AsyncIterator

from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from starlette.requests import Request
from starlette.responses import Response

from app.core.security import decode_token
from app.domain.entities.audit_log import AuditAction
from app.infrastructure.db.session import AsyncSessionLocal
from app.infrastructure.repositories.sqlalchemy_audit_repository import SqlAlchemyAuditRepository
from app.use_cases.audit.record_audit_event import RecordAuditEventInput, RecordAuditEventUseCase

_AUDITED_METHODS = {
    "POST": AuditAction.CREATE,
    "PUT": AuditAction.UPDATE,
    "PATCH": AuditAction.UPDATE,
    "DELETE": AuditAction.DELETE,
}
_UUID_RE = re.compile(r"^[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12}$")


class AuditMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next: RequestResponseEndpoint) -> Response:
        action = _AUDITED_METHODS.get(request.method)
        if action is None:
            return await call_next(request)

        response = await call_next(request)
        if response.status_code >= 400:
            return response

        body_chunks = [chunk async for chunk in response.body_iterator]
        response.body_iterator = _replay(body_chunks)

        try:
            await self._record(request, action, body_chunks)
        except Exception:  # noqa: BLE001 - auditing must never break the actual request
            pass

        return response

    async def _record(self, request: Request, action: AuditAction, body_chunks: list[bytes]) -> None:
        entity_type, entity_id = _extract_entity_info(request.url.path)
        if entity_id is None:
            entity_id = _extract_id_from_body(body_chunks)
        if entity_id is None:
            return

        async with AsyncSessionLocal() as session:
            use_case = RecordAuditEventUseCase(SqlAlchemyAuditRepository(session))
            await use_case.execute(
                RecordAuditEventInput(
                    action=action,
                    entity_type=entity_type,
                    entity_id=entity_id,
                    user_id=_extract_user_id(request),
                    ip_address=request.client.host if request.client else None,
                )
            )
            await session.commit()


def _extract_entity_info(path: str) -> tuple[str, uuid.UUID | None]:
    segments = [segment for segment in path.split("/") if segment]
    api_index = segments.index("v1") if "v1" in segments else -1
    resource_segments = segments[api_index + 1 :] if api_index >= 0 else segments

    entity_type = resource_segments[0] if resource_segments else "unknown"
    entity_id = None
    if len(resource_segments) > 1 and _UUID_RE.match(resource_segments[1]):
        entity_id = uuid.UUID(resource_segments[1])

    return entity_type, entity_id


def _extract_id_from_body(body_chunks: list[bytes]) -> uuid.UUID | None:
    try:
        payload = json.loads(b"".join(body_chunks) or b"{}")
    except (json.JSONDecodeError, UnicodeDecodeError):
        return None

    raw_id = payload.get("id") if isinstance(payload, dict) else None
    try:
        return uuid.UUID(raw_id) if raw_id else None
    except (ValueError, TypeError):
        return None


def _extract_user_id(request: Request) -> uuid.UUID | None:
    auth_header = request.headers.get("authorization", "")
    if not auth_header.lower().startswith("bearer "):
        return None

    token = auth_header.split(" ", 1)[1]
    try:
        payload = decode_token(token)
        return uuid.UUID(payload["sub"])
    except (ValueError, KeyError):
        return None


async def _replay(chunks: list[bytes]) -> AsyncIterator[bytes]:
    for chunk in chunks:
        yield chunk
