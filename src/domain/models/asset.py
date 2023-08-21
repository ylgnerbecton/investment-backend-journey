from sqlalchemy import Column, Float, String

from src.infrastructure.db import BaseModel


class AssetModel(BaseModel):
    __tablename__ = "assets"
    name = Column(String(255), nullable=False)
    current_price = Column(Float, nullable=False)
    category = Column(String(255), nullable=False)
    symbol = Column(String(255), nullable=False, unique=True)
