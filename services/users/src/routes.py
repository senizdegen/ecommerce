from fastapi import APIRouter, status, HTTPException, Depends
from typing import List
from .schemas import UserProfileModel
from .service import UserService
from .database import get_session
from sqlalchemy.ext.asyncio import AsyncSession
import uuid
from .dependencies import AccessTokenBearer

users_router = APIRouter()
user_service = UserService()

access_token_bearer = AccessTokenBearer()


@users_router.get("/", response_model=List[UserProfileModel])
async def get_users(
    session: AsyncSession = Depends(get_session),
    token_details=Depends(access_token_bearer),
):
    user_profiles = await user_service.get_users(session)
    return user_profiles


@users_router.get("/{user_uid}", response_model=UserProfileModel)
async def get_users(
    user_uid: str,
    session: AsyncSession = Depends(get_session),
    token_details=Depends(access_token_bearer),
):
    try:
        # just to validate
        valid_uid = uuid.UUID(user_uid)
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid user uid was provided",
        )

    user_profile = await user_service.get_user_by_uid(user_uid, session)
    if user_profile is not None:
        return user_profile
    else:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User with provided uid not found",
        )
