from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select, desc
from .models import UserProfile
from .schemas import UserProfileCreateModel, UserProfileUpdateModel
from datetime import datetime


class UserService:
    async def get_user_by_email(self, email: str, session: AsyncSession):
        statement = select(UserProfile).where(UserProfile.email == email)
        result = await session.execute(statement)
        return result.scalars().first()

    async def user_profile_exists(self, email: str, session: AsyncSession) -> bool:
        user_profile = await self.get_user_by_email(email, session)
        return user_profile is not None

    async def get_users(self, session: AsyncSession):
        statement = select(UserProfile).order_by(desc(UserProfile.created_at))
        result = await session.execute(statement)
        return result.scalars().all()

    async def get_user_by_uid(self, user_uid: str, session: AsyncSession):
        statement = select(UserProfile).where(UserProfile.uid == user_uid)
        result = await session.execute(statement)
        return result.scalars().first()

    async def create_user(self, user_data: UserProfileCreateModel, session: AsyncSession):
        new_user_profile = UserProfile(**user_data.model_dump())
        session.add(new_user_profile)
        await session.commit()
        await session.refresh(new_user_profile)
        return new_user_profile

    async def update_user(self, user_uid: str, update_data: UserProfileUpdateModel, session: AsyncSession):
        user = await self.get_user_by_uid(user_uid, session)
        if user is None:
            return None
        if update_data.first_name is not None:
            user.first_name = update_data.first_name
        if update_data.last_name is not None:
            user.last_name = update_data.last_name
        if update_data.email is not None:
            user.email = update_data.email
        if update_data.is_admin is not None:
            user.is_admin = update_data.is_admin
        user.updated_at = datetime.now()
        session.add(user)
        await session.commit()
        await session.refresh(user)
        return user

    async def delete_user(self, user_uid: str, session: AsyncSession):
        user = await self.get_user_by_uid(user_uid, session)
        if user is None:
            return None
        await session.delete(user)
        await session.commit()
        return {}