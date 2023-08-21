import bcrypt

from sqlalchemy import (
    Column,
    Float,
    ForeignKey,
    DateTime,
    String,
    CheckConstraint,
    Integer,
)
from sqlalchemy.orm import relationship, validates

from src.infrastructure.db import BaseModel


class UserModel(BaseModel):
    __tablename__ = "users"
    name = Column(String(255), nullable=False)
    cpf = Column(String(255), unique=True, nullable=False)
    email = Column(String(255), unique=True, nullable=False, index=True)
    _password = Column("password", String(60), nullable=False)
    birthdate = Column(DateTime, nullable=False)
    phone = Column(String(255), nullable=False)

    @validates("email")
    def validate_email(self, key, email):
        if "@" not in email:
            raise ValueError("Invalid email format")
        return email

    @validates("name")
    def validate_name(self, key, name):
        if not name or len(name.strip()) == 0:
            raise ValueError("Name can't be empty.")
        return name

    @validates("cpf")
    def validate_cpf(self, key, cpf):
        if len(cpf) != 11 or not cpf.isdigit():
            raise ValueError("CPF must have exactly 11 digits.")
        return cpf

    @property
    def password(self):
        raise AttributeError("Password is not readable.")

    @password.setter
    def password(self, plain_password):
        self._password = bcrypt.hashpw(
            plain_password.encode("utf-8"), bcrypt.gensalt()
        ).decode("utf-8")

    def verify_password(self, plain_password):
        return bcrypt.checkpw(
            plain_password.encode("utf-8"), self._password.encode("utf-8")
        )


class UserSessionModel(BaseModel):
    __tablename__ = "user_sessions"
    user_uuid = Column(String(36), ForeignKey("users.uuid"), nullable=False)
    token = Column(String(255), nullable=False, unique=True)
    expires_at = Column(DateTime, nullable=False)

    user = relationship("UserModel", backref="sessions")


class WalletModel(BaseModel):
    __tablename__ = "wallets"
    branch = Column(Integer, nullable=False)
    account = Column(String(255), unique=True, nullable=False)
    balance = Column(Float, CheckConstraint("balance>=0"), nullable=False, default=0.0)
    user_uuid = Column(String(36), ForeignKey("users.uuid"))

    transfers = relationship("TransferModel", back_populates="wallet")
    orders = relationship("OrderModel", back_populates="wallet")


class AuditLogModel(BaseModel):
    __tablename__ = "audit_logs"
    user_uuid = Column(String(36), ForeignKey("users.uuid"), nullable=True)
    action = Column(String(255), nullable=False)
    details = Column(String(255), nullable=True)

    user = relationship("UserModel", backref="logs")
