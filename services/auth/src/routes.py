from fastapi import APIRouter, HTTPException, status, Depends
from sqlmodel.ext.asyncio.session import AsyncSession
from .database import get_session
from .schemas import UserCreateModel, AuthUserModel
from .service import AuthService

auth_router = APIRouter()
auth_serviec = AuthService()

@auth_router.post('/signup')
async def register_user(user_data: UserCreateModel, session: AsyncSession = Depends(get_session)):
    new_user = await auth_serviec.create_user(user_data, session)
    return new_user