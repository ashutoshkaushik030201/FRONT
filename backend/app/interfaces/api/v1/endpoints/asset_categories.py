from typing import Annotated

from fastapi import APIRouter, Depends, Security

from app.domain.entities.user import User
from app.domain.repositories.asset_category_repository import AssetCategoryRepository
from app.interfaces.api.v1.deps import get_asset_category_repository, get_current_active_user
from app.interfaces.api.v1.schemas.asset_category_schemas import AssetCategoryResponse

router = APIRouter(prefix="/asset-categories", tags=["asset-categories"])


@router.get("", response_model=list[AssetCategoryResponse])
async def list_asset_categories(
    category_repo: Annotated[AssetCategoryRepository, Depends(get_asset_category_repository)],
    _current_user: Annotated[User, Security(get_current_active_user)],
) -> list[AssetCategoryResponse]:
    categories = await category_repo.list()
    return [AssetCategoryResponse.model_validate(category) for category in categories]
