from datetime import datetime

from sqlalchemy import (
    Column,
    Integer,
    Float,
    ForeignKey,
    DateTime,
    Enum,
    String,
    CheckConstraint,
)
from sqlalchemy.orm import relationship, validates

from src.infrastructure.db import BaseModel
from src.domain.constants import TransferType, Status


class TransferModel(BaseModel):
    __tablename__ = "transfers"
    wallet_uuid = Column(String(36), ForeignKey("wallets.uuid"))
    amount = Column(Float, CheckConstraint("amount>=0"), nullable=False)
    bank_origin = Column(String(255), nullable=False)
    agency_origin = Column(String(255), nullable=False)
    cpf_origin = Column(String(255))
    transfer_type = Column(Enum(TransferType), nullable=False)
    status = Column(Enum(Status), nullable=False)
    date = Column(DateTime, default=datetime.now)

    wallet = relationship("WalletModel", back_populates="transfers")

    @validates("amount")
    def validate_amount(self, key, amount):
        if amount < 0:
            raise ValueError("Transfer amount can't be negative.")
        return amount


class OrderModel(BaseModel):
    __tablename__ = "orders"
    wallet_uuid = Column(String(36), ForeignKey("wallets.uuid"))
    asset_uuid = Column(String(36), ForeignKey("assets.uuid"))
    amount = Column(Float, CheckConstraint("amount>=0"), nullable=False)
    price = Column(Float, CheckConstraint("price>=0"), nullable=False)
    status = Column(Enum(Status), nullable=False)

    wallet = relationship("WalletModel", back_populates="orders")

    @validates("price")
    def validate_price(self, key, price):
        if price < 0:
            raise ValueError("Asset price can't be negative.")
        return price
