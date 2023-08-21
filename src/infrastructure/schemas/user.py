from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel

from src.infrastructure.schemas import CustomBaseSchema


class UserBaseSchema(CustomBaseSchema):
    name: str
    cpf: str
    email: str
    phone: str
    birthdate: datetime


class UserCreateSchema(UserBaseSchema):
    password: str


class UserUpdateSchema(UserBaseSchema):
    pass


class UserResponseSchema(UserBaseSchema):
    pass


class UserSessionBaseSchema(CustomBaseSchema):
    user_uuid: str
    token: str
    expires_at: datetime


class UserSessionCreateSchema(UserSessionBaseSchema):
    pass


class UserSessionUpdateSchema(UserSessionBaseSchema):
    pass


class UserSessionResponseSchema(UserSessionBaseSchema):
    pass


class AccountBaseSchema(CustomBaseSchema):
    user_uuid: str


class AccountCreateSchema(AccountBaseSchema):
    pass


class AccountUpdateSchema(AccountBaseSchema):
    pass


class AccountResponseSchema(AccountBaseSchema):
    pass


class WalletBaseSchema(CustomBaseSchema):
    balance: Optional[float]
    branch: Optional[int]
    account: Optional[str]
    user_uuid: str


class WalletCreateSchema(WalletBaseSchema):
    pass


class WalletUpdateSchema(WalletBaseSchema):
    pass


class WalletResponseSchema(WalletBaseSchema):
    pass


class AuditLogBaseSchema(CustomBaseSchema):
    user_uuid: Optional[str]
    action: str
    details: Optional[str]


class AuditLogCreateSchema(AuditLogBaseSchema):
    pass


class AuditLogUpdateSchema(AuditLogBaseSchema):
    pass


class AuditLogResponseSchema(AuditLogBaseSchema):
    pass


class UserPositionSchema(BaseModel):
    symbol: str
    amount: float
    current_price: float
    order_value: float


class UserPositionResponseSchema(BaseModel):
    checking_account_amount: float
    positions: List[UserPositionSchema]
    consolidated: float
