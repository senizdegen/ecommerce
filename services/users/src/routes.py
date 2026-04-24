from fastapi import APIRouter, status, HTTPException, Depends
from typing import List
from .schemas import UserProfileModel, UserProfileUpdateModel
from .service import UserService
from .database import get_session
from sqlalchemy.ext.asyncio import AsyncSession
import uuid
from .dependencies import AccessTokenBearer, AdminBearer

users_router = APIRouter()
user_service = UserService()
access_token_bearer = AccessTokenBearer()
admin_bearer = AdminBearer()


@users_router.get("/", response_model=List[UserProfileModel])
async def get_users(
    session: AsyncSession = Depends(get_session),
    token_details=Depends(admin_bearer),  # только админ
):
    return await user_service.get_users(session)


@users_router.get("/{user_uid}", response_model=UserProfileModel)
async def get_user(
    user_uid: str,
    session: AsyncSession = Depends(get_session),
    token_details=Depends(access_token_bearer),
):
    try:
        uuid.UUID(user_uid)
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid user uid was provided",
        )
    user_profile = await user_service.get_user_by_uid(user_uid, session)
    if user_profile is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User with provided uid not found",
        )
    return user_profile


@users_router.patch("/{user_uid}", response_model=UserProfileModel)
async def update_user(
    user_uid: str,
    update_data: UserProfileUpdateModel,
    session: AsyncSession = Depends(get_session),
    token_details=Depends(access_token_bearer),
):
    current_uid = token_details["user"]["user_uid"]
    is_admin = token_details["user"].get("is_admin", False)

    if current_uid != user_uid and not is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You can only update your own profile"
        )

    # is_admin поле может менять только админ
    if update_data.is_admin is not None and not is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only admins can change admin status"
        )

    updated = await user_service.update_user(user_uid, update_data, session)
    if updated is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    return updated


@users_router.delete("/{user_uid}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(
    user_uid: str,
    session: AsyncSession = Depends(get_session),
    token_details=Depends(access_token_bearer),
):
    current_uid = token_details["user"]["user_uid"]
    is_admin = token_details["user"].get("is_admin", False)

    if current_uid != user_uid and not is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You can only delete your own account"
        )

    result = await user_service.delete_user(user_uid, session)
    if result is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    return {}