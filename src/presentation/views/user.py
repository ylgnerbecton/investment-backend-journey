from typing import Type, TypeVar
from http import HTTPStatus
from fastapi import APIRouter, HTTPException, status

from src.infrastructure.schemas import (
    UserBaseSchema,
    UserCreateSchema,
    UserUpdateSchema,
    UserResponseSchema,
    ResponseObjectSchema,
    UserPositionResponseSchema,
)
from src.domain.services import UserService
from .base import CRUDView


class UserView(CRUDView):
    resource_endpoint = "user"
    service_layer = UserService()
    base_schema = UserBaseSchema
    create_schema = UserCreateSchema
    update_schema = UserUpdateSchema
    response_schema = UserResponseSchema

    @classmethod
    def setup(cls):
        super().setup()

        @cls.router.get(
            f"/{cls.resource_endpoint}/position/{{uuid}}",
            tags=[cls.resource_endpoint],
            status_code=status.HTTP_200_OK,
            response_model=ResponseObjectSchema[UserPositionResponseSchema],
            description="Retrieve User's Asset Positions",
        )
        async def retrieve_user_position(uuid: str):
            try:
                return await cls.service_layer.user_position(user_uuid=uuid)
            except Exception as e:
                raise HTTPException(
                    detail=str(e), status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
                )
