from pydantic import BaseModel, Field, validator
from typing import Optional
from datetime import datetime
from decimal import Decimal
import re
import uuid

from app.models.user import UserGender, UserLevel


class UserBase(BaseModel):
    phone_number: str = Field(..., min_length=10, max_length=20, description="휴대폰 번호")
    nickname: str = Field(..., min_length=2, max_length=10, description="닉네임")
    gender: UserGender = Field(..., description="성별")
    age: int = Field(..., ge=10, le=100, description="나이")
    weight: Decimal = Field(..., ge=30, le=200, decimal_places=2, description="체중 (kg)")
    height: Decimal = Field(..., ge=100, le=250, decimal_places=2, description="키 (cm)")
    level: UserLevel = Field(..., description="운동 수준")

    @validator('phone_number')
    def validate_phone_number(cls, v):
        phone_pattern = re.compile(r'^01[0-9]-?[0-9]{4}-?[0-9]{4}$')
        if not phone_pattern.match(v.replace('-', '')):
            raise ValueError('올바른 휴대폰 번호 형식이 아닙니다')
        return v

    @validator('nickname')
    def validate_nickname(cls, v):
        if not re.match(r'^[가-힣a-zA-Z0-9_]+$', v):
            raise ValueError('닉네임은 한글, 영문, 숫자, 언더스코어만 사용 가능합니다')
        return v


class UserCreate(UserBase):
    password: str = Field(..., min_length=6, description="비밀번호 (6자 이상, 숫자 포함)")

    @validator('password')
    def validate_password(cls, v):
        if not re.search(r'\d', v):
            raise ValueError('비밀번호는 숫자를 포함해야 합니다')
        if len(v) < 6:
            raise ValueError('비밀번호는 6자 이상이어야 합니다')
        return v


class UserUpdate(BaseModel):
    nickname: Optional[str] = Field(None, min_length=2, max_length=10)
    age: Optional[int] = Field(None, ge=10, le=100)
    weight: Optional[Decimal] = Field(None, ge=30, le=200, decimal_places=2)
    height: Optional[Decimal] = Field(None, ge=100, le=250, decimal_places=2)
    level: Optional[UserLevel] = None

    @validator('nickname')
    def validate_nickname(cls, v):
        if v and not re.match(r'^[가-힣a-zA-Z0-9_]+$', v):
            raise ValueError('닉네임은 한글, 영문, 숫자, 언더스코어만 사용 가능합니다')
        return v


class UserResponse(UserBase):
    id: uuid.UUID
    is_active: bool
    is_verified: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class UserLogin(BaseModel):
    phone_number: str = Field(..., description="휴대폰 번호")
    password: str = Field(..., description="비밀번호")


class Token(BaseModel):
    access_token: str
    token_type: str
    refresh_token: str


class TokenData(BaseModel):
    user_id: Optional[str] = None