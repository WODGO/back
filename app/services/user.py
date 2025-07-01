from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from fastapi import HTTPException, status
from typing import Optional

from app.models.user import User
from app.schemas.user import UserCreate, UserUpdate
from app.services.auth import get_password_hash


async def create_user(db: AsyncSession, user_create: UserCreate) -> User:
    # 중복 휴대폰 번호 확인
    result = await db.execute(select(User).where(User.phone_number == user_create.phone_number))
    if result.scalar_one_or_none():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="이미 등록된 휴대폰 번호입니다"
        )
    
    # 중복 닉네임 확인
    result = await db.execute(select(User).where(User.nickname == user_create.nickname))
    if result.scalar_one_or_none():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="이미 사용 중인 닉네임입니다"
        )
    
    # 비밀번호 해시화
    hashed_password = get_password_hash(user_create.password)
    
    # 사용자 생성
    db_user = User(
        phone_number=user_create.phone_number,
        nickname=user_create.nickname,
        gender=user_create.gender,
        age=user_create.age,
        weight=user_create.weight,
        height=user_create.height,
        password_hash=hashed_password,
        level=user_create.level
    )
    
    db.add(db_user)
    await db.commit()
    await db.refresh(db_user)
    
    return db_user


async def get_user_by_id(db: AsyncSession, user_id: str) -> Optional[User]:
    result = await db.execute(select(User).where(User.id == user_id))
    return result.scalar_one_or_none()


async def get_user_by_phone_number(db: AsyncSession, phone_number: str) -> Optional[User]:
    result = await db.execute(select(User).where(User.phone_number == phone_number))
    return result.scalar_one_or_none()


async def update_user(db: AsyncSession, user_id: str, user_update: UserUpdate) -> Optional[User]:
    result = await db.execute(select(User).where(User.id == user_id))
    user = result.scalar_one_or_none()
    
    if not user:
        return None
    
    # 닉네임 중복 확인 (본인 제외)
    if user_update.nickname and user_update.nickname != user.nickname:
        result = await db.execute(
            select(User).where(
                User.nickname == user_update.nickname,
                User.id != user_id
            )
        )
        if result.scalar_one_or_none():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="이미 사용 중인 닉네임입니다"
            )
    
    # 업데이트할 필드들
    update_data = user_update.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(user, field, value)
    
    await db.commit()
    await db.refresh(user)
    
    return user