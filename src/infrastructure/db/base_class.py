import uuid

from datetime import datetime

from sqlalchemy.orm import declarative_base
from sqlalchemy import Column, DateTime, String, Boolean

Base = declarative_base()


class BaseModel(Base):
    __abstract__ = True
    uuid = Column(
        String(36),
        primary_key=True,
        default=lambda: str(uuid.uuid4()),
        unique=True,
        nullable=False,
    )
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)
    deleted = Column(Boolean, default=False)

    def __repr__(self):
        return f"{type(self).__name__}[{self.uuid}]"
