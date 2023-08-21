import logging

from typing import List, Optional, Tuple
from sqlalchemy.exc import SQLAlchemyError

from src.domain.models import WalletModel, OrderModel, AssetModel
from src.application.errors import GenericError, NotFoundError
from src.domain.constants import TransferType, Status
from src.infrastructure.db import DatabaseConnectionHandler
from src.infrastructure.schemas import (
    OrderBaseSchema,
    OrderCreateSchema,
    OrderUpdateSchema,
    OrderResponseSchema,
    WalletCreateSchema,
    PaginationParams,
)
from .repository import RepositoryCRUD

logging.basicConfig(
    level=logging.INFO,
    format="[%(asctime)s] %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
logger = logging.getLogger(__name__)


class OrderRepository(RepositoryCRUD[OrderBaseSchema]):

    async def create(self, data: OrderCreateSchema) -> OrderBaseSchema:
        user = "77f16dc1-dfec-46b3-83d2-5c1719b757e4"
        with DatabaseConnectionHandler() as db_connection:
            try:
                asset = (
                    db_connection.session.query(AssetModel)
                    .filter(AssetModel.symbol == data.symbol)
                    .first()
                )
                if not asset:
                    raise NotFoundError("Asset was not found.")

                current_price = asset.current_price

                total_cost = data.amount * current_price

                wallet = (
                    db_connection.session.query(WalletModel)
                    .filter(WalletModel.user_uuid == user)
                    .first()
                )
                logger.info(f"Query Result: {wallet.balance} and {total_cost}")

                if wallet.balance < total_cost:
                    raise GenericError("Insufficient funds.")

                wallet.balance -= total_cost
                current_balance = wallet.balance

                entity = OrderModel(
                    wallet_uuid=wallet.uuid,
                    asset_uuid=asset.uuid,
                    amount=data.amount,
                    price=current_price,
                    status=Status.Completed,
                )
                db_connection.session.add(entity)
                db_connection.session.flush()
                db_connection.session.commit()

                entity = (
                    db_connection.session.query(OrderModel)
                    .filter_by(uuid=entity.uuid)
                    .one()
                )
                order_data = OrderBaseSchema(
                    wallet_uuid=entity.wallet_uuid,
                    symbol=data.symbol,
                    amount=entity.amount,
                    price=entity.price,
                    status=entity.status,
                    asset_uuid=entity.asset_uuid,
                    current_balance=current_balance,
                )
                return order_data
            except SQLAlchemyError as error:
                db_connection.session.rollback()
                raise error

    async def retrieve_by_uuid(self, entity_uuid: str) -> Optional[OrderBaseSchema]:
        return await self._retrieve_by_uuid(OrderModel, entity_uuid)

    async def retrieve_all(
        self, pagination: PaginationParams
    ) -> Tuple[List[OrderBaseSchema], int, int]:
        return await self._retrieve_all(OrderModel, pagination)

    async def update(
        self, entity_uuid: str, data: OrderUpdateSchema
    ) -> Optional[OrderBaseSchema]:
        return await self._update(OrderModel, entity_uuid, data)

    async def delete(self, entity_uuid: str) -> bool:
        return await self._delete(OrderModel, entity_uuid)
