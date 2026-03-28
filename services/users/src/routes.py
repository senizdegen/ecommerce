from fastapi import APIRouter, status, HTTPException, Depends
from typing import List
from .schemas import UserProfileModel
from .service import UserService
from .database import get_session
from sqlalchemy.ext.asyncio import AsyncSession

users_router = APIRouter()
user_service = UserService()

@users_router.get('/', response_model=List[UserProfileModel])
async def get_users(session: AsyncSession = Depends(get_session)):
    user_profiles = await user_service.get_users(session)
    return user_profiles

