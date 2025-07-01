from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.schemas.user import UserResponse, UserUpdate
from app.services.user import get_user_by_id, update_user
from app.services.auth import get_current_user_dependency
from app.models.user import User

router = APIRouter(prefix="/users", tags=["Users"])


@router.get("/me", response_model=UserResponse)
async def get_current_user_profile(
    current_user: User = Depends(get_current_user_dependency)
):
    """
    현재 로그인한 사용자의 프로필 조회
    """
    return current_user


@router.put("/me", response_model=UserResponse)
async def update_current_user_profile(
    user_update: UserUpdate,
    current_user: User = Depends(get_current_user_dependency),
    db: AsyncSession = Depends(get_db)
):
    """
    현재 로그인한 사용자의 프로필 수정
    
    - **nickname**: 닉네임 (2-10자)
    - **age**: 나이 (10-100세)
    - **weight**: 체중 (30-200kg)
    - **height**: 키 (100-250cm)
    - **level**: 운동 수준 (초급/중급/고급/엘리트)
    """
    try:
        updated_user = await update_user(db, str(current_user.id), user_update)
        if not updated_user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="사용자를 찾을 수 없습니다"
            )
        return updated_user
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="프로필 수정 중 오류가 발생했습니다"
        )


@router.get("/{user_id}", response_model=UserResponse)
async def get_user_profile(
    user_id: str,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user_dependency)
):
    """
    특정 사용자 프로필 조회 (관리자용)
    """
    user = await get_user_by_id(db, user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="사용자를 찾을 수 없습니다"
        )
    return user