from fastapi import APIRouter, HTTPException, status
from typing import Dict, Any

from app.schemas.user import UserCreate, UserLogin, Token
from app.services.user_supabase import create_user_supabase, authenticate_user_supabase
from app.services.auth import create_access_token, create_refresh_token

router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.post("/register", status_code=status.HTTP_201_CREATED)
async def register_user(user_create: UserCreate) -> Dict[str, Any]:
    """
    회원가입
    
    - **phone_number**: 휴대폰 번호 (예: 01012345678)
    - **nickname**: 닉네임 (2-10자)
    - **gender**: 성별 (MALE/FEMALE)
    - **age**: 나이 (10-100세)
    - **weight**: 체중 (30-200kg)
    - **height**: 키 (100-250cm)
    - **password**: 비밀번호 (6자 이상, 숫자 포함)
    - **level**: 운동 수준 (초급/중급/고급/엘리트)
    """
    try:
        user = await create_user_supabase(user_create)
        return {
            "status": "success",
            "message": "회원가입이 완료되었습니다",
            "data": {
                "id": user["id"],
                "phone_number": user["phone_number"],
                "nickname": user["nickname"],
                "gender": user["gender"],
                "age": user["age"],
                "weight": user["weight"],
                "height": user["height"],
                "level": user["level"],
                "created_at": user["created_at"]
            }
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"회원가입 중 오류가 발생했습니다: {str(e)}"
        )


@router.post("/login", response_model=Token)
async def login_user(user_login: UserLogin):
    """
    로그인
    
    - **phone_number**: 휴대폰 번호
    - **password**: 비밀번호
    """
    user = await authenticate_user_supabase(user_login.phone_number, user_login.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="휴대폰 번호 또는 비밀번호가 올바르지 않습니다",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    if not user.get("is_active", True):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="비활성화된 계정입니다"
        )
    
    access_token = create_access_token(data={"sub": str(user["id"])})
    refresh_token = create_refresh_token(data={"sub": str(user["id"])})
    
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "refresh_token": refresh_token
    }