from .schemas import UserCreateModel, UserUpdateModel
from sqlmodel.ext.asyncio.session import AsyncSession
from .models import AuthUser
from sqlmodel import select
from .utils import generate_password_hash
from datetime import datetime


class AuthService():
    async def create_user(self, user_data: UserCreateModel, session: AsyncSession):
        hashed_password = generate_password_hash(user_data.password)
        new_user = AuthUser(
            email=user_data.email,
            password_hash=hashed_password,
        )
        session.add(new_user)
        await session.commit()
        await session.refresh(new_user)
        return new_user

    async def get_user_by_email(self, email: str, session: AsyncSession):
        statement = select(AuthUser).where(AuthUser.email == email)
        result = await session.exec(statement)
        return result.first()

    async def get_user_by_uid(self, uid: str, session: AsyncSession):
        statement = select(AuthUser).where(AuthUser.uid == uid)
        result = await session.exec(statement)
        return result.first()

    async def user_exists(self, email: str, session: AsyncSession):
        user = await self.get_user_by_email(email, session)
        return user is not None

    async def update_user(self, uid: str, update_data: UserUpdateModel, session: AsyncSession):
        user = await self.get_user_by_uid(uid, session)
        if user is None:
            return None
        if update_data.email is not None:
            user.email = update_data.email
        if update_data.password is not None:
            user.password_hash = generate_password_hash(update_data.password)
        user.updated_at = datetime.now()
        await session.commit()
        await session.refresh(user)
        return user

    async def delete_user(self, uid: str, session: AsyncSession):
        user = await self.get_user_by_uid(uid, session)
        if user is None:
            return None
        await session.delete(user)
        await session.commit()
        return {}