import uuid

from sqlalchemy import Column, String
from sqlalchemy.dialects.postgresql import UUID

from app.database.connection import Base


class Year(Base):
    __tablename__ = "year"

    guid = Column(UUID(as_uuid=True), default=uuid.uuid4, primary_key=True, index=True, unique=True)
    name = Column(String(32), unique=True, nullable=False)
