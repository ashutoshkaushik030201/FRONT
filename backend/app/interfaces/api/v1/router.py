from fastapi import APIRouter

from app.interfaces.api.v1.endpoints import asset_categories, assets, auth, users

api_router = APIRouter(prefix="/api/v1")
api_router.include_router(auth.router)
api_router.include_router(users.router)
api_router.include_router(asset_categories.router)
api_router.include_router(assets.router)
