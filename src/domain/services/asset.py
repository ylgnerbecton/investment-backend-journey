import logging

from src.domain.services.service import ServiceCRUD
from src.infrastructure.repositories import AssetRepository
from src.infrastructure.schemas import (
    Response,
    PaginationParams,
    ResponseListSchema,
    ResponseListWithPaginationSchema,
    AssetBaseSchema,
    AssetCreateSchema,
    AssetUpdateSchema,
    AssetResponseSchema,
)

logging.basicConfig(
    level=logging.INFO,
    format="[%(asctime)s] %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
logger = logging.getLogger(__name__)


class AssetService(ServiceCRUD[AssetBaseSchema]):
    def __init__(self) -> None:
        super().__init__(AssetRepository())
        logger.info(f"AssetService initialized in service layer.")

    async def create(self, data: AssetCreateSchema) -> Response:
        logger.info(f"Starting create asset method in AssetService.")
        return await self._create(data)

    async def retrieve_by_uuid(self, entity_uuid: str) -> Response:
        logger.info(
            f"Starting retrieve_by_uuid method in AssetService for UUID: {entity_uuid}."
        )
        return await self._retrieve_by_uuid(entity_uuid)

    async def retrieve_all(self, pagination: PaginationParams) -> ResponseListWithPaginationSchema:
        logger.info(
            f"Starting retrieve_all method in AssetService with pagination: {pagination.skip} - {pagination.limit}."
        )
        return await self._retrieve_all(pagination)

    async def update(self, entity_uuid: str, data: AssetUpdateSchema) -> Response:
        logger.info(f"Starting update method in AssetService for UUID: {entity_uuid}.")
        return await self._update(entity_uuid, data)

    async def delete(self, entity_uuid: str) -> Response:
        logger.info(f"Starting delete method in AssetService for UUID: {entity_uuid}.")
        return await self._delete(entity_uuid)

    async def retrieve_most_traded_assets(self) -> ResponseListSchema:
        logger.info(f"Starting retrieve_most_traded_assets in AssetService.")
        entities = await AssetRepository().retrieve_most_traded_assets()
        logger.info(f"Retrieved {len(entities)} most traded assets from the repository.")
        response_data = ResponseListSchema.build(entities)
        logger.info(f"Completed retrieve_most_traded_assets in AssetService.")
        return response_data
