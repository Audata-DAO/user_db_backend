from fastapi import APIRouter, Depends, HTTPException
from sqlmodel.ext.asyncio.session import AsyncSession

from app.core.db import get_db
from app.domains.users.models import User, UserMetadata
from app.domains.users.schemas import UserIn, UserMetadataIn
from app.domains.users.utils import create_user, create_user_metadata, get_user, get_user_metadata

router = APIRouter(prefix="/users", tags=["users"])


@router.post("/signup", response_model=User)
async def signup(user_in: UserIn, session: AsyncSession = Depends(get_db)):
    # check if user already exists
    user = await get_user(user_in.address, session)
    if user:
        raise HTTPException(status_code=400, detail="Пользователь уже зарегистрирован!")

    user = await create_user(user_in, session)
    return user


@router.post("/metadata", response_model=UserMetadata)
async def create_user_metadata_route(user_metadata_in: UserMetadataIn, session: AsyncSession = Depends(get_db)):
    user_metadata = await create_user_metadata(user_metadata_in, session)
    return user_metadata


@router.get("/metadata/")
async def get_user_metadata_route(user_wallet_address: str, session: AsyncSession = Depends(get_db)):
    r = await get_user_metadata(user_wallet_address, session)

    return r[0]
