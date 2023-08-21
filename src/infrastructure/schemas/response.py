from datetime import datetime
from uuid import uuid4
from typing import TypeVar, Generic, Type, List, Optional
from pydantic import BaseModel, Field, UUID4
from pydantic.generics import GenericModel

DataT = TypeVar("DataT")


class Response(GenericModel, Generic[DataT]):
    server_unix_timestamp: int = Field(
        default_factory=lambda: int(datetime.now().timestamp()),
        description="Server's Unix timestamp at the moment of the response",
    )
    response_data: DataT = Field(..., description="The response data")

    @classmethod
    def build(cls: Type["Response[DataT]"], response: DataT):
        return cls(response_data=response)


class ResponseObjectSchema(Response[DataT], Generic[DataT]):
    pass


class PaginationParams(BaseModel):
    skip: int = Field(0, description="Number of entries to skip for pagination")
    limit: int = Field(100, description="Maximum number of entries to return")


class ResponseListSchema(Response[List[DataT]], Generic[DataT]):
    pass


class ResponseListWithPaginationSchema(Response[List[DataT]], Generic[DataT]):
    skip: Optional[int] = Field(
        None, description="Number of entries to skip for pagination"
    )
    limit: Optional[int] = Field(
        None, description="Maximum number of entries to return"
    )
    total: Optional[int] = Field(None, description="Total number of entries")
    total_with_pagination: Optional[int] = Field(
        None, description="Maximum number of entries to return"
    )

    @classmethod
    def build_with_pagination(
        cls: Type["ResponseListWithPaginationSchema[DataT]"],
        response: DataT,
        pagination: PaginationParams,
        total,
        total_with_pagination,
    ):
        return cls(
            response_data=response,
            skip=pagination.skip,
            limit=pagination.limit,
            total=total,
            total_with_pagination=total_with_pagination,
        )


class CustomBaseSchema(BaseModel):
    uuid: Optional[UUID4] = Field(
        default_factory=lambda: uuid4(), description="UUID of the unique identifier"
    )
    created_at: datetime = Field(
        default_factory=datetime.utcnow,
        description="Timestamp of when the record was created",
    )
    updated_at: datetime = Field(
        default_factory=datetime.utcnow,
        description="Timestamp of when the record was last updated",
    )
    deleted: Optional[bool] = Field(
        default=False, description="Flag to mark if the record is deleted"
    )

    def dict(self, *args, **kwargs):
        return super().dict(*args, **kwargs)

    class Config:
        orm_mode = True
