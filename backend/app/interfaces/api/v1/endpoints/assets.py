import uuid
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Query, Security, status

from app.domain.entities.asset import AssetStatus
from app.domain.entities.user import RoleName, User
from app.domain.exceptions import DuplicateEntityError, EntityNotFoundError, InvalidOperationError
from app.domain.repositories.asset_repository import AssetRepository
from app.domain.repositories.depreciation_schedule_repository import DepreciationScheduleRepository
from app.interfaces.api.v1.deps import (
    get_asset_repository,
    get_assign_asset_use_case,
    get_calculate_depreciation_use_case,
    get_create_asset_use_case,
    get_current_active_user,
    get_depreciation_schedule_repository,
    get_list_assets_use_case,
    get_update_asset_use_case,
)
from app.interfaces.api.v1.schemas.asset_schemas import (
    AssetAssignmentResponse,
    AssetAssignRequest,
    AssetCreateRequest,
    AssetResponse,
    AssetUpdateRequest,
    DepreciationScheduleResponse,
)
from app.interfaces.api.v1.schemas.common import PaginatedResponse
from app.use_cases.asset.assign_asset import AssignAssetInput, AssignAssetUseCase
from app.use_cases.asset.calculate_depreciation import CalculateDepreciationUseCase
from app.use_cases.asset.create_asset import CreateAssetInput, CreateAssetUseCase
from app.use_cases.asset.list_assets import ListAssetsUseCase
from app.use_cases.asset.update_asset import UpdateAssetInput, UpdateAssetUseCase

router = APIRouter(prefix="/assets", tags=["assets"])

_WRITE_ROLES = [RoleName.ADMIN.value, RoleName.MANAGER.value]


@router.get("", response_model=PaginatedResponse[AssetResponse])
async def list_assets(
    use_case: Annotated[ListAssetsUseCase, Depends(get_list_assets_use_case)],
    _current_user: Annotated[User, Security(get_current_active_user)],
    page: int = Query(default=1, ge=1),
    page_size: int = Query(default=20, ge=1, le=100),
    search: str | None = Query(default=None, description="Full-text search across name/description/asset_tag"),
    category_id: uuid.UUID | None = None,
    status_filter: Annotated[AssetStatus | None, Query(alias="status")] = None,
    sort_by: str | None = Query(default=None, description="name|asset_tag|purchase_date|purchase_cost|created_at|status"),
    sort_order: str = Query(default="asc", pattern="^(asc|desc)$"),
) -> PaginatedResponse[AssetResponse]:
    result = await use_case.execute(
        page=page,
        page_size=page_size,
        search=search,
        category_id=category_id,
        status=status_filter.value if status_filter else None,
        sort_by=sort_by,
        sort_order=sort_order,
    )
    return PaginatedResponse(
        items=[AssetResponse.model_validate(asset) for asset in result.items],
        total=result.total,
        page=result.page,
        page_size=result.page_size,
    )


@router.post("", response_model=AssetResponse, status_code=status.HTTP_201_CREATED)
async def create_asset(
    payload: AssetCreateRequest,
    use_case: Annotated[CreateAssetUseCase, Depends(get_create_asset_use_case)],
    _current_user: Annotated[User, Security(get_current_active_user, scopes=_WRITE_ROLES)],
) -> AssetResponse:
    try:
        asset = await use_case.execute(CreateAssetInput(**payload.model_dump()))
    except DuplicateEntityError as exc:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(exc)) from exc
    return AssetResponse.model_validate(asset)


@router.get("/{asset_id}", response_model=AssetResponse)
async def get_asset(
    asset_id: uuid.UUID,
    asset_repo: Annotated[AssetRepository, Depends(get_asset_repository)],
    _current_user: Annotated[User, Security(get_current_active_user)],
) -> AssetResponse:
    asset = await asset_repo.get_by_id(asset_id)
    if asset is None or asset.is_deleted:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Asset not found")
    return AssetResponse.model_validate(asset)


@router.patch("/{asset_id}", response_model=AssetResponse)
async def update_asset(
    asset_id: uuid.UUID,
    payload: AssetUpdateRequest,
    use_case: Annotated[UpdateAssetUseCase, Depends(get_update_asset_use_case)],
    _current_user: Annotated[User, Security(get_current_active_user, scopes=_WRITE_ROLES)],
) -> AssetResponse:
    try:
        asset = await use_case.execute(asset_id, UpdateAssetInput(**payload.model_dump(exclude_unset=True)))
    except EntityNotFoundError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc
    return AssetResponse.model_validate(asset)


@router.post(
    "/{asset_id}/assign",
    response_model=AssetAssignmentResponse,
    status_code=status.HTTP_201_CREATED,
)
async def assign_asset(
    asset_id: uuid.UUID,
    payload: AssetAssignRequest,
    use_case: Annotated[AssignAssetUseCase, Depends(get_assign_asset_use_case)],
    _current_user: Annotated[User, Security(get_current_active_user, scopes=_WRITE_ROLES)],
) -> AssetAssignmentResponse:
    try:
        assignment = await use_case.execute(
            AssignAssetInput(asset_id=asset_id, user_id=payload.user_id, notes=payload.notes)
        )
    except EntityNotFoundError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc
    except InvalidOperationError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc)) from exc
    return AssetAssignmentResponse.model_validate(assignment)


@router.get("/{asset_id}/depreciation", response_model=list[DepreciationScheduleResponse])
async def get_depreciation_schedule(
    asset_id: uuid.UUID,
    schedule_repo: Annotated[DepreciationScheduleRepository, Depends(get_depreciation_schedule_repository)],
    _current_user: Annotated[User, Security(get_current_active_user)],
) -> list[DepreciationScheduleResponse]:
    schedules = await schedule_repo.list_by_asset(asset_id)
    return [DepreciationScheduleResponse.model_validate(s) for s in schedules]


@router.post("/{asset_id}/depreciation/recalculate", response_model=list[DepreciationScheduleResponse])
async def recalculate_depreciation(
    asset_id: uuid.UUID,
    use_case: Annotated[CalculateDepreciationUseCase, Depends(get_calculate_depreciation_use_case)],
    _current_user: Annotated[User, Security(get_current_active_user, scopes=_WRITE_ROLES)],
) -> list[DepreciationScheduleResponse]:
    try:
        schedules = await use_case.execute(asset_id)
    except EntityNotFoundError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc
    return [DepreciationScheduleResponse.model_validate(s) for s in schedules]
