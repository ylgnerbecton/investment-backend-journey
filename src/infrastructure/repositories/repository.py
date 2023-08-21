import logging

from pydantic import BaseModel

from typing import List, Optional, Tuple, Type, TypeVar

from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm.exc import NoResultFound

from src.domain.interfaces import (
    RepositoryCRUDInterface,
    RepositoryCreateInterface,
    RepositoryRetrieveByUUIDInterface,
    RepositoryRetrieveAllInterface,
    RepositoryUpdateInterface,
    RepositoryDeleteInterface,
)
from src.infrastructure.db import DatabaseConnectionHandler
from src.infrastructure.schemas import PaginationParams
from src.application.errors import NotFoundError

logging.basicConfig(
    level=logging.INFO,
    format="[%(asctime)s] %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
logger = logging.getLogger(__name__)

T = TypeVar("T", bound=BaseModel)


class RepositoryCreate(RepositoryCreateInterface[T]):
    async def _create(self, model: Type[T], data: BaseModel) -> T:
        with DatabaseConnectionHandler() as db_connection:
            try:
                entity = model(**data.dict())
                db_connection.session.add(entity)
                db_connection.session.flush()
                db_connection.session.commit()
                entity = (
                    db_connection.session.query(model).filter_by(uuid=entity.uuid).one()
                )
                logger.info(f"{model.__name__} created successfully.")
                return entity
            except SQLAlchemyError as error:
                logger.error(f"Error creating {model.__name__}: {error}")
                db_connection.session.rollback()
                raise error


class RepositoryRetrieveByUUID(RepositoryRetrieveByUUIDInterface[T]):
    async def _retrieve_by_uuid(self, model: Type[T], entity_uuid: str) -> Optional[T]:
        with DatabaseConnectionHandler() as db_connection:
            try:
                entity = (
                    db_connection.session.query(model).filter_by(uuid=entity_uuid).one()
                )
                logger.info(f"{model.__name__} data retrieved for UUID: {entity_uuid}.")
                return entity
            except NoResultFound:
                logger.warning(
                    f"No {model.__name__} data found for UUID: {entity_uuid}."
                )
                raise NotFoundError


class RepositoryRetrieveAll(RepositoryRetrieveAllInterface[T]):
    async def _retrieve_all(
        self, model: Type[T], pagination: PaginationParams
    ) -> Tuple[List[T], int, int]:
        with DatabaseConnectionHandler() as db_connection:
            entities = (
                db_connection.session.query(model)
                .offset(pagination.skip)
                .limit(pagination.limit)
                .all()
            )
            total = db_connection.session.query(model).count()
            total_with_pagination = len(entities)
            logger.info(
                f"{model.__name__} data retrieved with pagination: {pagination.skip} - {pagination.limit}."
            )
            return entities, total, total_with_pagination


class RepositoryUpdate(RepositoryUpdateInterface[T]):
    async def _update(
        self, model: Type[T], entity_uuid: str, data: BaseModel
    ) -> Optional[T]:
        with DatabaseConnectionHandler() as db_connection:
            try:
                entity = (
                    db_connection.session.query(model).filter_by(uuid=entity_uuid).one()
                )
                update_data = data.dict(exclude_unset=True)
                for key, value in update_data.items():
                    setattr(entity, key, value)
                db_connection.session.add(entity)
                db_connection.session.commit()
                logger.info(f"{model.__name__} data updated for UUID: {entity_uuid}.")
                return entity
            except NoResultFound:
                logger.warning(
                    f"No {model.__name__} data found for UUID: {entity_uuid} for update."
                )
                raise NotFoundError
            except SQLAlchemyError as error:
                logger.error(
                    f"Error updating {model.__name__} data for UUID {entity_uuid}: {error}"
                )
                db_connection.session.rollback()
                raise error


class RepositoryDelete(RepositoryDeleteInterface[T]):
    async def _delete(self, model: Type[T], entity_uuid: str) -> bool:
        with DatabaseConnectionHandler() as db_connection:
            try:
                deleted = (
                    db_connection.session.query(model)
                    .filter_by(uuid=entity_uuid)
                    .delete(synchronize_session=False)
                )
                db_connection.session.commit()
                if deleted > 0:
                    logger.info(
                        f"{model.__name__} data with UUID {entity_uuid} deleted successfully."
                    )
                    return True
                logger.warning(
                    f"{model.__name__} data with UUID {entity_uuid} not found for deletion."
                )
                return False
            except SQLAlchemyError as error:
                logger.error(
                    f"Error deleting {model.__name__} data with UUID {entity_uuid}: {error}"
                )
                db_connection.session.rollback()
                raise error


class RepositoryCRUD(
    RepositoryCreate[T],
    RepositoryRetrieveByUUID[T],
    RepositoryRetrieveAll[T],
    RepositoryUpdate[T],
    RepositoryDelete[T],
):
    pass
