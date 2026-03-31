from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select, desc
from .models import UserProfile
from .schemas import UserProfileCreateModel

class UserService:
    async def get_user_by_email(self, email: str, session: AsyncSession):
        statement = select(UserProfile).where(UserProfile.email == email)
        result = await session.execute(statement)
        user_profile = result.scalars().first()
        return user_profile
    
    async def user_profile_exists(self, email: str, session: AsyncSession) -> bool:
        user_profile = await self.get_user_by_email(email, session)
        return True if user_profile is not None else False
    
    async def get_users(self, session: AsyncSession):
        statement = select(UserProfile).order_by(desc(UserProfile.created_at))
        result = await session.execute(statement)
        return result.scalars().all()
    
    async def get_user_by_uid(self, user_uid: str, session:AsyncSession):
        statement = select(UserProfile).where(UserProfile.uid == user_uid)
        result = await session.execute(statement)
        if result:
            return result.scalars().first()
        else:
            return None
        
    async def create_user(self, user_data: UserProfileCreateModel, session: AsyncSession):
        user_data_dict = user_data.model_dump()
        new_user_profile = UserProfile(
            **user_data_dict
        )
        session.add(new_user_profile)
        await session.commit()
        await session.refresh(new_user_profile)

        return new_user_profile