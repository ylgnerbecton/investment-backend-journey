from typing import Type, TypeVar
from http import HTTPStatus
from fastapi import APIRouter, HTTPException, status

from src.infrastructure.schemas import (
    AssetBaseSchema,
    AssetCreateSchema,
    AssetUpdateSchema,
    AssetResponseSchema,
    ResponseObjectSchema,
    ResponseListSchema,
    MostTradedAssetSchema,
)
from src.domain.services import AssetService
from .base import CRUDView


class AssetView(CRUDView):
    resource_endpoint = "asset"
    service_layer = AssetService()
    base_schema = AssetBaseSchema
    create_schema = AssetCreateSchema
    update_schema = AssetUpdateSchema
    response_schema = AssetResponseSchema

    @classmethod
    def setup(cls):
        @cls.router.get(
            f"/{cls.resource_endpoint}/trends",
            tags=[cls.resource_endpoint],
            status_code=status.HTTP_200_OK,
            response_model=ResponseListSchema[MostTradedAssetSchema],
            description="API for the Top 5 Most Traded Assets",
        )
        async def trends_assets():
            try:
                return await cls.service_layer.retrieve_most_traded_assets()
            except Exception as e:
                raise HTTPException(
                    detail=str(e), status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
                )

        super().setup()
