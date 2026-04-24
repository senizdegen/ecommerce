from fastapi import APIRouter, HTTPException, status, Depends, Request
from fastapi.responses import JSONResponse
from sqlmodel.ext.asyncio.session import AsyncSession
from .database import get_session
from .schemas import UserCreateModel, AuthUserModel, UserLoginModel, UserUpdateModel
from .service import AuthService
from .utils import verify_password, create_access_token, decode_token
from .dependencies import AccessTokenBearer, AdminBearer

auth_router = APIRouter()
auth_service = AuthService()
access_token_bearer = AccessTokenBearer()
admin_bearer = AdminBearer()


@auth_router.post("/signup", status_code=status.HTTP_201_CREATED)
async def register_user(
    user_data: UserCreateModel,
    request: Request,
    session: AsyncSession = Depends(get_session),
):
    email = user_data.email
    user_exists = await auth_service.user_exists(email, session)
    if user_exists:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User with provided email already exists",
        )
    new_user = await auth_service.create_user(user_data, session)
    await request.app.state.rabbit.publish_user_created({
        "uid": str(new_user.uid),
        "first_name": user_data.first_name,
        "last_name": user_data.last_name,
        "email": new_user.email,
        "is_admin": new_user.is_admin,
    })
    return {
        "message": "User created successfully",
        "user": {
            "uid": str(new_user.uid),
            "email": new_user.email,
        },
    }


@auth_router.post("/login")
async def login_user(
    login_data: UserLoginModel,
    session: AsyncSession = Depends(get_session)
):
    email = login_data.email
    password = login_data.password
    user = await auth_service.get_user_by_email(email, session)
    if user is not None:
        password_valid = verify_password(password, user.password_hash)
        if password_valid:
            access_token = create_access_token(
                user_data={
                    "email": email,
                    "user_uid": str(user.uid),
                    "is_admin": user.is_admin,  # добавить в токен
                }
            )
            refresh_token = create_access_token(
                user_data={
                    "email": email,
                    "user_uid": str(user.uid),
                    "is_admin": user.is_admin,
                },
                refresh=True
            )
            return JSONResponse(content={
                "message": "Login is successfull",
                "access_token": access_token,
                "refresh_token": refresh_token,
                "user": {"uid": str(user.uid), "email": user.email},
            })
    raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail="Invalid credentials"
    )


@auth_router.patch("/{user_uid}", response_model=AuthUserModel)
async def update_user(
    user_uid: str,
    update_data: UserUpdateModel,
    request: Request,
    session: AsyncSession = Depends(get_session),
    token_details: dict = Depends(access_token_bearer),
):
    # юзер может менять только себя, админ — любого
    current_uid = token_details["user"]["user_uid"]
    is_admin = token_details["user"].get("is_admin", False)

    if current_uid != user_uid and not is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You can only update your own account"
        )

    updated_user = await auth_service.update_user(user_uid, update_data, session)
    if updated_user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )

    await request.app.state.rabbit.publish_user_updated({
        "uid": str(updated_user.uid),
        "email": updated_user.email,
        "is_admin": updated_user.is_admin,
    })

    return updated_user


@auth_router.delete("/{user_uid}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(
    user_uid: str,
    request: Request,
    session: AsyncSession = Depends(get_session),
    token_details: dict = Depends(access_token_bearer),
):
    current_uid = token_details["user"]["user_uid"]
    is_admin = token_details["user"].get("is_admin", False)

    if current_uid != user_uid and not is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You can only delete your own account"
        )

    result = await auth_service.delete_user(user_uid, session)
    if result is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )

    await request.app.state.rabbit.publish_user_deleted({
        "uid": user_uid
    })

    return {}