from fastapi import APIRouter, Depends
from sqlmodel.ext.asyncio.session import AsyncSession

from app.core.db import get_db
from app.domains.users.models import User
from app.domains.users.schemas import UserIn
from app.domains.users.utils import create_user

router = APIRouter(prefix="/users", tags=["users"])


@router.post("/signup", response_model=User)
async def signup(user_in: UserIn, session: AsyncSession = Depends(get_db)):
    user = await create_user(user_in, session)
    return user
