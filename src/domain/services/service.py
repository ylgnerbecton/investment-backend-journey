import logging
from pydantic import BaseModel
from typing import TypeVar

from src.domain.interfaces import (
    ServiceCRUDInterface,
    ServiceCreateInterface,
    ServiceRetrieveByUUIDInterface,
    ServiceRetrieveAllInterface,
    ServiceUpdateInterface,
    ServiceDeleteInterface,
)
from src.infrastructure.schemas import (
    Response,
    PaginationParams,
    ResponseListWithPaginationSchema,
)
from src.application.errors import NotFoundError

T = TypeVar("T")
U = TypeVar("U", bound=BaseModel)

logging.basicConfig(
    level=logging.INFO,
    format="[%(asctime)s] %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
logger = logging.getLogger(__name__)


class BaseService:
    def __init__(self, repository: T, service_name: str = "Service") -> None:
        self.repository = repository
        self.service_name = service_name
        logger.info(f"{self.service_name} initialized in service layer.")


class ServiceCreate(BaseService, ServiceCreateInterface[T]):
    async def _create(self, data: U) -> Response:
        entity = await self.repository.create(data)
        logger.info(f"{self.service_name} created successfully in service layer.")
        return Response.build(entity)


class ServiceRetrieveByUUID(BaseService, ServiceRetrieveByUUIDInterface[T]):
    async def _retrieve_by_uuid(self, entity_uuid: str) -> Response:
        entity = await self.repository.retrieve_by_uuid(entity_uuid)
        if not entity:
            logger.warning(
                f"{self.service_name} not found for UUID: {entity_uuid} in service layer."
            )
            raise NotFoundError(f"{self.service_name} not found")
        logger.info(
            f"{self.service_name} retrieved for UUID: {entity_uuid} in service layer."
        )
        return Response.build(entity)


class ServiceRetrieveAll(BaseService, ServiceRetrieveAllInterface[T]):
    async def _retrieve_all(
        self, pagination: PaginationParams
    ) -> ResponseListWithPaginationSchema:
        entities, total, total_with_pagination = await self.repository.retrieve_all(
            pagination
        )
        logger.info(
            f"{self.service_name} data retrieved with pagination: {pagination.skip} - {pagination.limit} in service layer."
        )
        response_data = ResponseListWithPaginationSchema.build_with_pagination(
            entities, pagination, total, total_with_pagination
        )
        logger.info(response_data)
        return response_data


class ServiceUpdate(BaseService, ServiceUpdateInterface[T]):
    async def _update(self, entity_uuid: str, data: U) -> Response:
        entity = await self.repository.update(entity_uuid, data)
        if not entity:
            logger.warning(
                f"{self.service_name} not found for UUID: {entity_uuid} for update in service layer."
            )
            raise NotFoundError(f"{self.service_name} not found")
        logger.info(
            f"{self.service_name} updated for UUID: {entity_uuid} in service layer."
        )
        return Response.build(entity)


class ServiceDelete(BaseService, ServiceDeleteInterface[T]):
    async def _delete(self, entity_uuid: str) -> Response:
        entity = await self.repository.retrieve_by_uuid(entity_uuid)
        if not entity:
            logger.warning(
                f"{self.service_name} not found for UUID: {entity_uuid} for deletion in service layer."
            )
            raise NotFoundError(f"{self.service_name} not found")
        await self.repository.delete(entity_uuid)
        logger.info(
            f"{self.service_name} with UUID {entity_uuid} deleted successfully in service layer."
        )
        return Response.build(entity)


class ServiceCRUD(
    ServiceCreate[T],
    ServiceRetrieveByUUID[T],
    ServiceRetrieveAll[T],
    ServiceUpdate[T],
    ServiceDelete[T],
):
    def __init__(self, repository: T, service_name: str = "ServiceCRUD"):
        super().__init__(repository, service_name)
