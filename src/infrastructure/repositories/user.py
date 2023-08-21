import logging

from typing import List, Optional, Tuple

from src.domain.models import UserModel, WalletModel, OrderModel, AssetModel
from src.infrastructure.db import DatabaseConnectionHandler
from src.domain.constants import Status
from src.infrastructure.schemas import (
    UserBaseSchema,
    UserCreateSchema,
    UserUpdateSchema,
    UserResponseSchema,
    WalletCreateSchema,
    PaginationParams,
    UserPositionResponseSchema,
)
from .repository import RepositoryCRUD

logging.basicConfig(
    level=logging.INFO,
    format="[%(asctime)s] %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
logger = logging.getLogger(__name__)


class UserRepository(RepositoryCRUD[UserBaseSchema]):
    async def create(self, data: UserCreateSchema) -> UserBaseSchema:
        user = await self._create(UserModel, data)
        if user:
            wallet_schema = WalletCreateSchema(user_uuid=user.uuid)
            await self._create(WalletModel, wallet_schema)
        return user

    async def retrieve_by_uuid(self, entity_uuid: str) -> Optional[UserBaseSchema]:
        return await self._retrieve_by_uuid(UserModel, entity_uuid)

    async def retrieve_all(
        self, pagination: PaginationParams
    ) -> Tuple[List[UserBaseSchema], int, int]:
        return await self._retrieve_all(UserModel, pagination)

    async def update(
        self, entity_uuid: str, data: UserUpdateSchema
    ) -> Optional[UserBaseSchema]:
        return await self._update(UserModel, entity_uuid, data)

    async def delete(self, entity_uuid: str) -> bool:
        return await self._delete(UserModel, entity_uuid)

    async def user_position(self, user_uuid: str) -> UserPositionResponseSchema:
        logger.info(f"Starting user_position method in UserService for user UUID: {user_uuid}.")

        with DatabaseConnectionHandler() as db_connection:
            logger.info(f"Querying wallet and orders for user UUID: {user_uuid}.")

            user_wallet = (
                db_connection.session.query(WalletModel)
                .join(UserModel)
                .filter(UserModel.uuid == user_uuid)
                .first()
            )

            if not user_wallet:
                logger.warning(f"No wallet found for user UUID: {user_uuid}. Returning empty data.")
                return UserPositionResponseSchema(checking_account_amount=0, positions=[], consolidated=0)

            checking_account_amount = user_wallet.balance

            orders = (
                db_connection.session.query(OrderModel)
                .filter(OrderModel.wallet_uuid == user_wallet.uuid)
                .all()
            )

            positions_dict = {}
            total_positions_value = 0

            for order in orders:
                if order.status != Status.Completed:
                    continue

                asset = (
                    db_connection.session.query(AssetModel)
                    .filter(AssetModel.uuid == order.asset_uuid)
                    .first()
                )
                asset_current_price = asset.current_price

                order_value = asset_current_price * order.amount
                total_positions_value += order_value

                if asset.symbol in positions_dict:
                    positions_dict[asset.symbol]["amount"] += order.amount
                    positions_dict[asset.symbol]["order_value"] += order_value
                else:
                    positions_dict[asset.symbol] = {
                        "symbol": asset.symbol,
                        "amount": order.amount,
                        "current_price": asset_current_price,
                        "order_value": order_value,
                    }

            positions_list = list(positions_dict.values())
            consolidated = checking_account_amount + total_positions_value

            response = UserPositionResponseSchema(
                checking_account_amount=checking_account_amount,
                positions=positions_list,
                consolidated=consolidated
            )

            logger.info(f"Successfully generated user position data for user UUID: {user_uuid}.")
            return response

