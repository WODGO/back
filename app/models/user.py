from sqlalchemy import Column, String, Integer, Boolean, DateTime, Enum, DECIMAL
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
import enum
import uuid

from app.core.database import Base


class UserGender(str, enum.Enum):
    MALE = "MALE"
    FEMALE = "FEMALE"


class UserLevel(str, enum.Enum):
    BEGINNER = "초급"
    INTERMEDIATE = "중급"
    ADVANCED = "고급"
    ELITE = "엘리트"


class User(Base):
    __tablename__ = "users"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    phone_number = Column(String(20), unique=True, nullable=False, index=True)
    nickname = Column(String(10), nullable=False, index=True)
    gender = Column(Enum(UserGender), nullable=False)
    age = Column(Integer, nullable=False)
    weight = Column(DECIMAL(5, 2), nullable=False)
    height = Column(DECIMAL(5, 2), nullable=False)
    password_hash = Column(String(255), nullable=False)
    level = Column(Enum(UserLevel), nullable=False)
    is_active = Column(Boolean, default=True)
    is_verified = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())