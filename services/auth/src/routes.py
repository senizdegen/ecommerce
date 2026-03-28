from fastapi import APIRouter, HTTPException, status, Depends, Request
from fastapi.responses import JSONResponse
from sqlmodel.ext.asyncio.session import AsyncSession
from .database import get_session
from .schemas import UserCreateModel, AuthUserModel, UserLoginModel
from .service import AuthService
from .utils import verify_password, create_access_token, decode_token

auth_router = APIRouter()
auth_service = AuthService()


@auth_router.post("/signup")
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
    await request.app.state.rabbit.publish_user_created(
        {
            "uid": str(new_user.uid),
            "first_name": user_data.first_name,
            "last_name": user_data.last_name,
            "email": new_user.email,
        }
    )
    return {
        "message": "User created successfully",
        "user": {
            "uid": str(new_user.uid),
            "email": new_user.email,
        },
    }


@auth_router.post("/login")
async def login_user(
    login_data: UserLoginModel, session: AsyncSession = Depends(get_session)
):
    email = login_data.email
    password = login_data.password

    user = await auth_service.get_user_by_email(email, session)
    if user is not None:
        password_valid = verify_password(password, user.password_hash)
        if password_valid:
            access_token = create_access_token(
                user_data={"email": email, "user_uid": str(user.uid)}
            )

            refresh_token = create_access_token(
                user_data={"email": email, "user_uid": str(user.uid)}, refresh=True
            )

            return JSONResponse(
                content={
                    "message": "Login is successfull",
                    "access_token": access_token,
                    "refresh_token": refresh_token,
                    "user": {"uid": str(user.uid), "email": user.email},
                }
            )

    else:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid credentials"
        )
