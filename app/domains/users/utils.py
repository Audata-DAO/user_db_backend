from fastapi import HTTPException
from sqlmodel.ext.asyncio.session import AsyncSession

from app.domains.users.models import User
from app.domains.users.schemas import UserIn


async def create_user(user_in: UserIn, session: AsyncSession) -> User:
    try:
        user = User(**user_in.model_dump())

        session.add(user)
        await session.commit()
        await session.refresh(user)

        return user
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
