from typing import Type, TypeVar
from http import HTTPStatus
from fastapi import APIRouter, HTTPException, status

from src.infrastructure.schemas import (
    OrderBaseSchema,
    OrderCreateSchema,
    OrderUpdateSchema,
    OrderResponseSchema,
    ResponseObjectSchema,
)
from src.domain.services import OrderService
from .base import CRUDView


class OrderView(CRUDView):
    resource_endpoint = "order"
    service_layer = OrderService()
    base_schema = OrderBaseSchema
    create_schema = OrderCreateSchema
    update_schema = OrderUpdateSchema
    response_schema = OrderResponseSchema


# from fastapi import FastAPI, HTTPException
# from src.infrastructure.db import DatabaseConnectionHandler
# from pydantic import BaseModel
#
# from src.domain.models import (
#     UserModel,
#     WalletModel,
#     AssetModel,
#     TransferModel,
#     OrderModel,
# )


# class TransferEventSchema(BaseModel):
#     event: str
#     target: dict
#     origin: dict
#     amount: float


# @health_check_router.post("/spb/events")
# async def transfer_event(event_data: TransferEventSchema):
#     account = event_data.target["account"]
#     origin_cpf = event_data.origin["cpf"]
#
#     with DatabaseConnectionHandler() as db_connection:
#         session = db_connection.session
#
#         user = (
#             session.query(UserModel)
#             .join(WalletModel)
#             .filter(WalletModel.account == account)
#             .first()
#         )
#         if not user:
#             raise HTTPException(status_code=404, detail="Account not found.")
#
#         if user.cpf != origin_cpf:
#             raise HTTPException(
#                 status_code=403, detail="Origin CPF does not match account holder."
#             )
#
#         wallet = session.query(WalletModel).filter_by(account=account).first()
#         if not wallet:
#             raise HTTPException(status_code=404, detail="Wallet not found.")
#
#         wallet.balance += event_data.amount
#         transfer_data = {
#             "wallet_uuid": wallet.uuid,
#             "amount": event_data.amount,
#             "bank_origin": event_data.origin["bank"],
#             "agency_origin": event_data.origin["branch"],
#             "cpf_origin": origin_cpf,
#             "transfer_type": "Deposit",
#             "status": "Completed",
#         }
#
#         transfer = TransferModel(**transfer_data)
#         session.add(transfer)
#         session.commit()
#
#         return {"message": "Transfer processed successfully!"}
