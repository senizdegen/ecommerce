from .schemas import UserCreateModel
from sqlmodel.ext.asyncio.session import AsyncSession
from .models import AuthUser
from .utils import generate_password_hash

class AuthService():
    async def create_user(self, user_data: UserCreateModel, session: AsyncSession):
        hashed_password = generate_password_hash(user_data.password)

        new_user = AuthUser(
            email=user_data.email,
            password_hash=hashed_password
        )

        session.add(new_user)

        await session.commit()
        await session.refresh(new_user)

        return new_user
    