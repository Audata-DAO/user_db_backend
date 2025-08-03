from fastapi import APIRouter

from app.core.db import SessionDep
from app.core.models import UserIn, Users

users_router = APIRouter(prefix="/users")


@users_router.post("/signup", response_model=Users)
async def signup(user_in: UserIn, session: SessionDep):
    user = Users(**user_in.model_dump())

    session.add(user)
    await session.commit()
    await session.refresh(user)

    return user
