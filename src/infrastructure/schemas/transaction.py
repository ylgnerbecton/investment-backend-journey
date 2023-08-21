from datetime import datetime
from typing import TypeVar, Generic, Type, List, Optional
from pydantic import BaseModel, conint, constr, Field, confloat, UUID4

from src.domain.constants import TransferType, Status
from src.infrastructure.schemas import CustomBaseSchema


class TransferBaseSchema(CustomBaseSchema):
    wallet_uuid: UUID4 = Field(
        ..., description="UUID of the wallet associated with the transfer"
    )
    amount: confloat(gt=0) = Field(
        ..., description="Amount of the transfer", example=100.50
    )
    bank_origin: constr(min_length=1) = Field(
        ..., description="Bank of origin", example="Bank XYZ"
    )
    agency_origin: constr(min_length=1) = Field(
        ..., description="Agency of origin", example="1234"
    )
    cpf_origin: constr(regex="^[0-9]{11}$") = Field(
        ..., description="CPF of the account holder", example="12345678901"
    )
    transfer_type: Optional[TransferType] = Field(
        ..., description="Type of transfer", example="Deposit"
    )


class TransferCreateSchema(TransferBaseSchema):
    pass


class TransferUpdateSchema(TransferBaseSchema):
    amount: confloat(gt=0) = Field(description="Amount of the transfer", example=100.50)


class TransferResponseSchema(TransferBaseSchema):
    uuid: UUID4 = Field(..., description="UUID of the transfer")
    status: Optional[Status] = Field(
        ..., description="Status of the transfer", example="Completed"
    )
    date: datetime = Field(..., description="Date of the transfer")


class OrderBaseSchema(CustomBaseSchema):
    wallet_uuid: UUID4 = Field(
        ..., description="UUID of the wallet associated with the order"
    )
    symbol: Optional[constr(min_length=1)] = Field(
        None, description="symbol of the asset being purchased"
    )
    amount: confloat(gt=0) = Field(
        ..., description="Amount of the asset being purchased", example=3.0
    )
    price: confloat(gt=0) = Field(
        ..., description="Price of the asset at the time of purchase", example=40.77
    )
    asset_uuid: Optional[UUID4] = Field(
        None, description="UUID of the asset being purchased"
    )
    status: Optional[Status] = Field(
        None, description="Status of the order", example="Completed"
    )
    current_balance: Optional[confloat(gt=0)] = Field(
        None, description="Price of the asset at the time of purchase", example=40.77
    )


class OrderCreateSchema(OrderBaseSchema):
    pass


class OrderUpdateSchema(OrderBaseSchema):
    amount: confloat(gt=0) = Field(
        description="Amount of the asset being purchased", example=3.0
    )
    price: confloat(gt=0) = Field(
        description="Price of the asset at the time of purchase", example=40.77
    )


class OrderResponseSchema(OrderBaseSchema):
    pass
