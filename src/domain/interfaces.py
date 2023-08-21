from typing import TypeVar, Generic, List, Optional, Tuple, Type
from abc import ABC, abstractmethod
from pydantic import BaseModel

from src.infrastructure.schemas import (
    Response,
    ResponseListWithPaginationSchema,
    PaginationParams,
)

T = TypeVar("T", bound=BaseModel)


class Interface(Generic[T], ABC):
    pass


class RepositoryCreateInterface(Interface[T]):
    @abstractmethod
    async def _create(self, model: Type[T], data: BaseModel) -> Optional[T]:
        """Create and return a new instance."""
        raise NotImplementedError


class RepositoryRetrieveByUUIDInterface(Interface[T]):
    @abstractmethod
    async def _retrieve_by_uuid(self, model: Type[T], entity_uuid: str) -> Optional[T]:
        """Retrieve and return an instance by its UUID."""
        raise NotImplementedError


class RepositoryRetrieveAllInterface(Interface[T]):
    @abstractmethod
    async def _retrieve_all(
        self, model: Type[T], pagination: PaginationParams
    ) -> Tuple[List[T], int, int]:
        """Retrieve and return all instances, with optional pagination."""
        raise NotImplementedError


class RepositoryUpdateInterface(Interface[T]):
    @abstractmethod
    async def _update(
        self, model: Type[T], entity_uuid: str, data: BaseModel
    ) -> Optional[T]:
        """Update an existing instance by its UUID and return the updated instance."""
        raise NotImplementedError


class RepositoryDeleteInterface(Interface[T]):
    @abstractmethod
    async def _delete(self, model: Type[T], entity_uuid: str) -> bool:
        """Delete an instance by its UUID."""
        raise NotImplementedError


class RepositoryCRUDInterface(
    RepositoryCreateInterface,
    RepositoryRetrieveByUUIDInterface,
    RepositoryRetrieveAllInterface,
    RepositoryUpdateInterface,
    RepositoryDeleteInterface,
    Generic[T],
    ABC,
):
    pass


class ServiceCreateInterface(Interface[T]):
    @abstractmethod
    async def _create(self, data: T) -> Optional[Response]:
        raise NotImplementedError


class ServiceRetrieveByUUIDInterface(Interface[T]):
    @abstractmethod
    async def _retrieve_by_uuid(self, entity_uuid: str) -> Optional[Response]:
        raise NotImplementedError


class ServiceRetrieveAllInterface(Interface[T]):
    @abstractmethod
    async def _retrieve_all(
        self, pagination: PaginationParams
    ) -> Optional[ResponseListWithPaginationSchema]:
        raise NotImplementedError


class ServiceUpdateInterface(Interface[T]):
    @abstractmethod
    async def _update(self, entity_uuid: str, data: T) -> Optional[Response]:
        raise NotImplementedError


class ServiceDeleteInterface(Interface[T]):
    @abstractmethod
    async def _delete(self, entity_uuid: str) -> Response:
        raise NotImplementedError


class ServiceCRUDInterface(
    ServiceCreateInterface,
    ServiceRetrieveByUUIDInterface,
    ServiceRetrieveAllInterface,
    ServiceUpdateInterface,
    ServiceDeleteInterface,
    Generic[T],
    ABC,
):
    pass
