from uuid import uuid4
from typing import Optional
from pydantic import BaseModel, Field, UUID4, constr, confloat

from src.infrastructure.schemas import CustomBaseSchema


class AssetBaseSchema(CustomBaseSchema):
    name: constr(min_length=1) = Field(..., description="Name of the asset")
    current_price: confloat(gt=0) = Field(
        ..., description="Current price of the asset", example=28.44
    )
    category: constr(min_length=1) = Field(..., description="Category of the asset")
    symbol: constr(min_length=1) = Field(
        ..., description="Symbol representing the asset", unique=True
    )


class AssetCreateSchema(AssetBaseSchema):
    pass


class AssetUpdateSchema(AssetBaseSchema):
    name: Optional[constr(min_length=1)] = Field(description="Name of the asset")
    current_price: Optional[confloat(gt=0)] = Field(
        description="Current price of the asset"
    )
    category: Optional[constr(min_length=1)] = Field(
        description="Category of the asset"
    )
    symbol: Optional[constr(min_length=1)] = Field(
        description="Symbol representing the asset"
    )


class AssetResponseSchema(AssetBaseSchema):
    pass


class MostTradedAssetSchema(BaseModel):
    uuid: Optional[UUID4] = Field(
        default_factory=lambda: uuid4(), description="UUID of the unique identifier"
    )
    current_price: confloat(gt=0) = Field(
        ..., description="Current price of the asset", example=28.44
    )
    symbol: constr(min_length=1) = Field(
        ..., description="Symbol representing the asset", unique=True
    )
