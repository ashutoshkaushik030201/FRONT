from fastapi import FastAPI, Request, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from app.core.config import get_settings
from app.core.exceptions import AppException
from app.core.logging import configure_logging
from app.domain.exceptions import (
    AuthenticationError,
    AuthorizationError,
    DomainError,
    DuplicateEntityError,
    EntityNotFoundError,
    InvalidOperationError,
)
from app.interfaces.api.v1.router import api_router
from app.interfaces.middleware.audit_middleware import AuditMiddleware

settings = get_settings()

_DOMAIN_ERROR_STATUS: dict[type[DomainError], int] = {
    EntityNotFoundError: status.HTTP_404_NOT_FOUND,
    DuplicateEntityError: status.HTTP_409_CONFLICT,
    AuthenticationError: status.HTTP_401_UNAUTHORIZED,
    AuthorizationError: status.HTTP_403_FORBIDDEN,
    InvalidOperationError: status.HTTP_400_BAD_REQUEST,
}


def create_app() -> FastAPI:
    configure_logging(level="DEBUG" if settings.environment == "local" else "INFO")

    app = FastAPI(title="Nexus API", version="0.1.0", openapi_url="/api/v1/openapi.json")

    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.cors_origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    app.add_middleware(AuditMiddleware)

    @app.exception_handler(AppException)
    async def app_exception_handler(_request: Request, exc: AppException) -> JSONResponse:
        return JSONResponse(
            status_code=exc.status_code,
            content={"error": {"code": exc.error_code, "message": exc.message, "details": exc.details}},
        )

    @app.exception_handler(DomainError)
    async def domain_exception_handler(_request: Request, exc: DomainError) -> JSONResponse:
        status_code = _DOMAIN_ERROR_STATUS.get(type(exc), status.HTTP_400_BAD_REQUEST)
        return JSONResponse(
            status_code=status_code,
            content={"error": {"code": exc.__class__.__name__, "message": str(exc), "details": {}}},
        )

    @app.get("/health", tags=["health"])
    async def health_check() -> dict[str, str]:
        return {"status": "ok"}

    app.include_router(api_router)

    return app


app = create_app()
