import logging

from src.domain.services.service import ServiceCRUD
from src.infrastructure.repositories import UserRepository
from src.infrastructure.schemas import (
    Response,
    PaginationParams,
    ResponseObjectSchema,
    ResponseListWithPaginationSchema,
    UserBaseSchema,
    UserCreateSchema,
    UserUpdateSchema,
    UserResponseSchema,
)

logging.basicConfig(
    level=logging.INFO,
    format="[%(asctime)s] %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
logger = logging.getLogger(__name__)


class UserService(ServiceCRUD[UserBaseSchema]):
    def __init__(self) -> None:
        super().__init__(UserRepository())
        logger.info(f"UserService initialized in service layer.")

    async def create(self, data: UserCreateSchema) -> Response:
        logger.info(f"Starting create user method in UserService.")
        return await self._create(data)

    async def retrieve_by_uuid(self, entity_uuid: str) -> Response:
        logger.info(
            f"Starting retrieve_by_uuid method in UserService for UUID: {entity_uuid}."
        )
        return await self._retrieve_by_uuid(entity_uuid)

    async def retrieve_all(
        self, pagination: PaginationParams
    ) -> ResponseListWithPaginationSchema:
        logger.info(
            f"Starting retrieve_all method in UserService with pagination: {pagination.skip} - {pagination.limit}."
        )
        return await self._retrieve_all(pagination)

    async def update(self, entity_uuid: str, data: UserUpdateSchema) -> Response:
        logger.info(f"Starting update method in UserService for UUID: {entity_uuid}.")
        return await self._update(entity_uuid, data)

    async def delete(self, entity_uuid: str) -> Response:
        logger.info(f"Starting delete method in UserService for UUID: {entity_uuid}.")
        return await self._delete(entity_uuid)

    async def user_position(self, user_uuid: str) -> ResponseObjectSchema:
        logger.info(f"Starting user_position in UserService.")
        entities = await self.repository.user_position(user_uuid)
        return ResponseObjectSchema.build(entities)
