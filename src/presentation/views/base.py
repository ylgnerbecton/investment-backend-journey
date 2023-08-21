import logging

from typing import Type, TypeVar
from fastapi import APIRouter, HTTPException, status, Depends
from pydantic import BaseModel

from src.application.errors import NotFoundError
from src.infrastructure.schemas import (
    ResponseListWithPaginationSchema,
    ResponseObjectSchema,
    PaginationParams,
)

T = TypeVar("T", bound=BaseModel)

logging.basicConfig(
    level=logging.INFO,
    format="[%(asctime)s] %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
logger = logging.getLogger(__name__)


class CRUDView:
    resource_endpoint: str
    service_layer: Type[T]
    base_schema: Type[T]
    create_schema: Type[T]
    update_schema: Type[T]
    response_schema: Type[T]

    router = APIRouter()

    _is_setup_done = False

    def __init__(self):
        self.router = APIRouter()

    @classmethod
    def setup(cls):
        if not cls._is_setup_done:
            cls.router.tags = [cls.resource_endpoint]
            cls._is_setup_done = True

        @cls.router.post(
            f"/{cls.resource_endpoint}",
            status_code=status.HTTP_201_CREATED,
            response_model=ResponseObjectSchema[cls.response_schema],
        )
        async def create_resource(request: cls.create_schema):
            return await cls._create_resource(request)

        @cls.router.get(
            f"/{cls.resource_endpoint}",
            status_code=status.HTTP_200_OK,
            response_model=ResponseListWithPaginationSchema[cls.response_schema],
        )
        async def retrieve_all_resources(pagination: PaginationParams = Depends()):
            return await cls._retrieve_resources(pagination)

        @cls.router.get(
            f"/{cls.resource_endpoint}/{{uuid}}",
            status_code=status.HTTP_200_OK,
            response_model=ResponseObjectSchema[cls.response_schema],
        )
        async def retrieve_resource_by_uuid(uuid: str):
            return await cls._retrieve_resource_by_uuid(uuid)

        @cls.router.put(
            f"/{cls.resource_endpoint}/{{uuid}}",
            status_code=status.HTTP_200_OK,
            response_model=ResponseObjectSchema[cls.update_schema],
        )
        async def update_resource(uuid: str, request: cls.update_schema):
            return await cls._update_resource(uuid, request)

        @cls.router.delete(
            f"/{cls.resource_endpoint}/{{uuid}}",
            status_code=status.HTTP_200_OK,
            response_model=ResponseObjectSchema[cls.response_schema],
        )
        async def delete_resource(uuid: str):
            return await cls._delete_resource(uuid)

    @classmethod
    def get_router(cls):
        cls.setup()
        return cls.router

    @classmethod
    async def _create_resource(cls, request):
        try:
            result = await cls.service_layer.create(data=request)
            logger.info(f"Item created successfully in {cls.resource_endpoint}.")
            return result
        except Exception as e:
            logger.error(f"Error while creating item in {cls.resource_endpoint}: {e}")
            raise HTTPException(
                detail=str(e), status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    @classmethod
    async def _retrieve_resources(cls, pagination: PaginationParams):
        try:
            result = await cls.service_layer.retrieve_all(pagination)
            logger.info(f"Items retrieved successfully from {cls.resource_endpoint}.")
            return result
        except Exception as e:
            logger.error(
                f"Error while retrieving items from {cls.resource_endpoint}: {e}"
            )
            raise HTTPException(
                detail=str(e), status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    @classmethod
    async def _retrieve_resource_by_uuid(cls, entity_uuid: str):
        try:
            result = await cls.service_layer.retrieve_by_uuid(entity_uuid=entity_uuid)
            logger.info(
                f"Item {entity_uuid} retrieved successfully from {cls.resource_endpoint}."
            )
            return result
        except NotFoundError as e:
            logger.error(
                f"Item not found in {cls.resource_endpoint} with UUID {entity_uuid}."
            )
            raise HTTPException(detail=e.description, status_code=e.code)
        except Exception as e:
            logger.error(
                f"Error while retrieving item from {cls.resource_endpoint} with UUID {entity_uuid}: {e}"
            )
            raise HTTPException(
                detail=str(e), status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    @classmethod
    async def _update_resource(cls, entity_uuid: str, request):
        try:
            result = await cls.service_layer.update(entity_uuid=entity_uuid, data=request)
            logger.info(
                f"Item {entity_uuid} updated successfully in {cls.resource_endpoint}."
            )
            return result
        except NotFoundError as e:
            logger.error(
                f"Item not found in {cls.resource_endpoint} while updating with UUID {entity_uuid}."
            )
            raise HTTPException(detail=e.description, status_code=e.code)
        except Exception as e:
            logger.error(
                f"Error while updating item in {cls.resource_endpoint} with UUID {entity_uuid}: {e}"
            )
            raise HTTPException(
                detail=str(e), status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    @classmethod
    async def _delete_resource(cls, entity_uuid: str):
        try:
            result = await cls.service_layer.delete(entity_uuid=entity_uuid)
            logger.info(
                f"Item {entity_uuid} deleted successfully from {cls.resource_endpoint}."
            )
            return result
        except NotFoundError as e:
            logger.error(
                f"Item not found in {cls.resource_endpoint} while deleting with UUID {entity_uuid}."
            )
            raise HTTPException(detail=e.description, status_code=e.code)
        except Exception as e:
            logger.error(
                f"Error while deleting item in {cls.resource_endpoint} with UUID {entity_uuid}: {e}"
            )
            raise HTTPException(
                detail=str(e), status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
