import logging

from src.domain.services.service import ServiceCRUD
from src.infrastructure.repositories import OrderRepository
from src.infrastructure.schemas import (
    Response,
    PaginationParams,
    ResponseObjectSchema,
    ResponseListWithPaginationSchema,
    OrderBaseSchema,
    OrderCreateSchema,
    OrderUpdateSchema,
    OrderResponseSchema,
)

logging.basicConfig(
    level=logging.INFO,
    format="[%(asctime)s] %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
logger = logging.getLogger(__name__)


class OrderService(ServiceCRUD[OrderBaseSchema]):
    def __init__(self) -> None:
        super().__init__(OrderRepository())
        logger.info(f"OrderService initialized in service layer.")

    async def create(self, data: OrderCreateSchema) -> Response:
        logger.info(f"Starting create user method in OrderService.")
        return await self._create(data)

    async def retrieve_by_uuid(self, entity_uuid: str) -> Response:
        logger.info(
            f"Starting retrieve_by_uuid method in OrderService for UUID: {entity_uuid}."
        )
        return await self._retrieve_by_uuid(entity_uuid)

    async def retrieve_all(
        self, pagination: PaginationParams
    ) -> ResponseListWithPaginationSchema:
        logger.info(
            f"Starting retrieve_all method in OrderService with pagination: {pagination.skip} - {pagination.limit}."
        )
        return await self._retrieve_all(pagination)

    async def update(self, entity_uuid: str, data: OrderUpdateSchema) -> Response:
        logger.info(f"Starting update method in OrderService for UUID: {entity_uuid}.")
        return await self._update(entity_uuid, data)

    async def delete(self, entity_uuid: str) -> Response:
        logger.info(f"Starting delete method in OrderService for UUID: {entity_uuid}.")
        return await self._delete(entity_uuid)
