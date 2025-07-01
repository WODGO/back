from typing import Optional, Dict, Any
from fastapi import HTTPException, status
import bcrypt
import uuid
from datetime import datetime

from app.core.supabase_client import supabase
from app.schemas.user import UserCreate, UserUpdate


async def create_user_supabase(user_create: UserCreate) -> Dict[str, Any]:
    """Supabase를 사용한 사용자 생성"""
    
    # 중복 휴대폰 번호 확인
    existing_user = supabase.table("users").select("id").eq("phone_number", user_create.phone_number).execute()
    if existing_user.data:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="이미 등록된 휴대폰 번호입니다"
        )
    
    # 중복 닉네임 확인
    existing_nickname = supabase.table("users").select("id").eq("nickname", user_create.nickname).execute()
    if existing_nickname.data:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="이미 사용 중인 닉네임입니다"
        )
    
    # 비밀번호 해시화
    password_bytes = user_create.password.encode('utf-8')
    hashed_password = bcrypt.hashpw(password_bytes, bcrypt.gensalt()).decode('utf-8')
    
    # 사용자 데이터 준비
    user_data = {
        "phone_number": user_create.phone_number,
        "nickname": user_create.nickname,
        "gender": user_create.gender.value,
        "age": user_create.age,
        "weight": float(user_create.weight),
        "height": float(user_create.height),
        "password_hash": hashed_password,
        "level": user_create.level.value,
        "is_active": True,
        "is_verified": False
    }
    
    # 사용자 생성
    result = supabase.table("users").insert(user_data).execute()
    
    if not result.data:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="사용자 생성에 실패했습니다"
        )
    
    return result.data[0]


async def get_user_by_phone_supabase(phone_number: str) -> Optional[Dict[str, Any]]:
    """휴대폰 번호로 사용자 조회"""
    result = supabase.table("users").select("*").eq("phone_number", phone_number).execute()
    return result.data[0] if result.data else None


async def get_user_by_id_supabase(user_id: str) -> Optional[Dict[str, Any]]:
    """ID로 사용자 조회"""
    result = supabase.table("users").select("*").eq("id", user_id).execute()
    return result.data[0] if result.data else None


async def authenticate_user_supabase(phone_number: str, password: str) -> Optional[Dict[str, Any]]:
    """사용자 인증"""
    user = await get_user_by_phone_supabase(phone_number)
    if not user:
        return None
    
    password_bytes = password.encode('utf-8')
    hashed_password = user['password_hash'].encode('utf-8')
    
    if not bcrypt.checkpw(password_bytes, hashed_password):
        return None
    
    return user


async def update_user_supabase(user_id: str, user_update: UserUpdate) -> Optional[Dict[str, Any]]:
    """사용자 정보 업데이트"""
    
    # 닉네임 중복 확인 (본인 제외)
    if user_update.nickname:
        existing_nickname = supabase.table("users").select("id").eq("nickname", user_update.nickname).neq("id", user_id).execute()
        if existing_nickname.data:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="이미 사용 중인 닉네임입니다"
            )
    
    # 업데이트할 데이터 준비
    update_data = {}
    if user_update.nickname is not None:
        update_data["nickname"] = user_update.nickname
    if user_update.age is not None:
        update_data["age"] = user_update.age
    if user_update.weight is not None:
        update_data["weight"] = float(user_update.weight)
    if user_update.height is not None:
        update_data["height"] = float(user_update.height)
    if user_update.level is not None:
        update_data["level"] = user_update.level.value
    
    if not update_data:
        # 업데이트할 데이터가 없으면 현재 사용자 정보 반환
        return await get_user_by_id_supabase(user_id)
    
    # 업데이트 실행
    result = supabase.table("users").update(update_data).eq("id", user_id).execute()
    
    if not result.data:
        return None
    
    return result.data[0]