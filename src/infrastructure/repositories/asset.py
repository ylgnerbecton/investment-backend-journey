import logging

from sqlalchemy import func
from datetime import datetime, timedelta
from typing import List, Optional, Tuple

from src.domain.models import AssetModel, OrderModel
from src.infrastructure.db import DatabaseConnectionHandler
from src.infrastructure.schemas import (
    AssetBaseSchema,
    AssetCreateSchema,
    AssetUpdateSchema,
    PaginationParams,
    MostTradedAssetSchema,
)
from .repository import RepositoryCRUD

logging.basicConfig(
    level=logging.INFO,
    format="[%(asctime)s] %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
logger = logging.getLogger(__name__)


class AssetRepository(RepositoryCRUD[AssetBaseSchema]):
    async def create(self, data: AssetCreateSchema) -> AssetBaseSchema:
        return await self._create(AssetModel, data)

    async def retrieve_by_uuid(self, entity_uuid: str) -> Optional[AssetBaseSchema]:
        return await self._retrieve_by_uuid(AssetModel, entity_uuid)

    async def retrieve_all(
        self, pagination: PaginationParams
    ) -> Tuple[List[AssetBaseSchema], int, int]:
        return await self._retrieve_all(AssetModel, pagination)

    async def update(
        self, entity_uuid: str, data: AssetUpdateSchema
    ) -> Optional[AssetBaseSchema]:
        return await self._update(AssetModel, entity_uuid, data)

    async def delete(self, entity_uuid: str) -> bool:
        return await self._delete(AssetModel, entity_uuid)

    async def retrieve_most_traded_assets(self) -> List[MostTradedAssetSchema]:
        logger.info(f"Starting retrieve_most_traded_assets method in AssetService.")
        seven_days_ago = datetime.now() - timedelta(days=7)

        with DatabaseConnectionHandler() as db_connection:
            logger.info("Querying for most traded assets from the past seven days.")
            most_traded_asset_orders = (
                db_connection.session.query(
                    OrderModel.asset_uuid,
                    func.count(OrderModel.asset_uuid).label("trade_count"),
                )
                .filter(OrderModel.created_at >= seven_days_ago)
                .filter(OrderModel.status == "Completed")
                .group_by(OrderModel.asset_uuid)
                .order_by(func.count(OrderModel.asset_uuid).desc())
                .limit(5)
                .all()
            )

            if not most_traded_asset_orders:
                logger.warning(
                    "No asset orders found in the past seven days. Returning empty list."
                )
                return []

            logger.info(
                f"Retrieved {len(most_traded_asset_orders)} asset orders from the database."
            )

            most_traded_assets = []
            for asset_order in most_traded_asset_orders:
                logger.debug(
                    f"Fetching asset details for UUID: {asset_order.asset_uuid}"
                )
                asset_data = (
                    db_connection.session.query(AssetModel)
                    .filter(AssetModel.uuid == asset_order.asset_uuid)
                    .first()
                )

                if not asset_data:
                    logger.warning(
                        f"No asset data found for UUID: {asset_order.asset_uuid}. Skipping..."
                    )
                    continue

                asset_instance = MostTradedAssetSchema(
                    uuid=asset_data.uuid,
                    current_price=asset_data.current_price,
                    symbol=asset_data.symbol
                )

                most_traded_assets.append(asset_instance)

            logger.info(
                f"Successfully generated list of {len(most_traded_assets)} most traded assets."
            )
            return most_traded_assets
