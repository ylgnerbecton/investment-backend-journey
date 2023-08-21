import logging
import jwt

from typing import Type, TypeVar

from fastapi import APIRouter, HTTPException, status, Depends
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel
from datetime import datetime, timedelta
from passlib.context import CryptContext

from src.domain.models import (
    UserModel,
    UserSessionModel,
)
from src.infrastructure.db import DatabaseConnectionHandler

logging.basicConfig(
    level=logging.INFO,
    format="[%(asctime)s] %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
logger = logging.getLogger(__name__)

T = TypeVar("T", bound=BaseModel)

auth_router = APIRouter(tags=["auth"])

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/token")


class AuthConfig:
    SECRET_KEY = "your-jwt-secret"
    ALGORITHM = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES = 30

    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

    @staticmethod
    def verify_password(plain_password, hashed_password):
        return AuthConfig.pwd_context.verify(plain_password, hashed_password)

    @staticmethod
    def get_password_hash(password):
        return AuthConfig.pwd_context.hash(password)

    @staticmethod
    def create_access_token(data: dict, expires_delta: timedelta = None):
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + timedelta(minutes=15)
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(
            to_encode, AuthConfig.SECRET_KEY, algorithm=AuthConfig.ALGORITHM
        )
        return encoded_jwt


class Token(BaseModel):
    access_token: str
    token_type: str


@auth_router.post(
    "/auth/token", status_code=status.HTTP_201_CREATED, response_model=Token
)
async def create_item(form_data: OAuth2PasswordRequestForm = Depends()):
    with DatabaseConnectionHandler() as db_connection:
        user = (
            db_connection.session.query(UserModel)
            .filter(UserModel.email == form_data.username)
            .first()
        )

        if not user or not AuthConfig.verify_password(
            form_data.password, user._password
        ):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect email or password",
                headers={"WWW-Authenticate": "Bearer"},
            )

        access_token_expires = timedelta(minutes=AuthConfig.ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = AuthConfig.create_access_token(
            data={"sub": user.email}, expires_delta=access_token_expires
        )

        session = UserSessionModel(
            user_uuid=user.uuid,
            token=access_token,
            expires_at=datetime.utcnow() + access_token_expires,
        )
        db_connection.session.add(session)
        db_connection.session.commit()

        logger.info(f"Token generated successfully for {user.email}.")
        return {"access_token": access_token, "token_type": "bearer"}
