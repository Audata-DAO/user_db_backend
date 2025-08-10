from fastapi import APIRouter, HTTPException

from app.domains.users import schemas
from app.core.db import SessionDep
from app.domains.users.models import User, UserMetadata
from app.domains.users import utils

router = APIRouter(prefix="/users", tags=["users"])


@router.post("/signup", response_model=User)
async def signup(user_in: schemas.UserIn, session: SessionDep):
    # check if user already exists
    user = await utils.get_user(user_in.address, session)
    if user:
        raise HTTPException(status_code=400, detail="Пользователь уже зарегистрирован!")

    user = await utils.create_user(user_in, session)
    return user


@router.post("/metadata", response_model=UserMetadata)
async def create_user_metadata_route(
    user_metadata_in: schemas.UserMetadataIn, session: SessionDep
):
    user_metadata = await utils.create_user_metadata(user_metadata_in, session)
    return user_metadata


@router.get("/metadata")
async def get_user_metadata_route(user_wallet_address: str, session: SessionDep):
    r = await utils.get_user_metadata(user_wallet_address, session)

    return r[0]


@router.post("/stat")
async def create_statistics_entry_route(
    user_statistics: schemas.UserStatisticsIn, session: SessionDep
):
    print(user_statistics)
    r = await utils.create_statistics_entry(user_statistics, session)
    return r
