import uuid

from pydantic import BaseModel


class AssetCategoryResponse(BaseModel):
    id: uuid.UUID
    name: str
    type: str

    model_config = {"from_attributes": True}
