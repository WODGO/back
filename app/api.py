from fastapi import APIRouter

from app.routers import auth_supabase, users

router = APIRouter()

router.include_router(auth_supabase.router)
router.include_router(users.router)