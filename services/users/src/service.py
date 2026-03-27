from sqlmodel.ext.asyncio.session import AsyncSession
from sqlmodel import select, desc
from .models import UserProfile

class UserService:
    async def get_user_by_email(self, email: str, session: AsyncSession):
        statement = select(UserProfile).where(UserProfile.email == email)
        result = await session.exec(statement)
        user_profile = result.first()
        return user_profile
    
    async def get_users(self, session: AsyncSession):
        statement = select(UserProfile).order_by(desc(UserProfile.created_at))
        result = await session.exec(statement)
        user_profiles = result.all()
        return user_profiles
