from fastapi import HTTPException
from sqlmodel import desc, select, text, func
from sqlalchemy.exc import IntegrityError, MultipleResultsFound, NoResultFound
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.ext.asyncio import AsyncSession

from app.domains.users.models import Emails, User, UserMetadata
from app.domains.users.schemas import (
    Leader,
    Leaders,
    StatisticsOut,
    UserIn,
    UserMetadataIn,
    UserStatisticsIn,
)


async def create_user(user_in: UserIn, session: AsyncSession) -> User:
    try:
        user = User(**user_in.model_dump())

        session.add(user)
        await session.commit()
        await session.refresh(user)

        return user
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


async def get_user(wallet_address: str, session: AsyncSession) -> User | None:
    statement = select(User).where(User.address == wallet_address)
    result = await session.execute(statement)
    return result.scalar_one_or_none()


"""===============РЕАЛИЗАЦИЯ С КООРДИНАТАМИ================================"""
# async def create_user_metadata(
#     user_metadata_in: UserMetadataIn, session: AsyncSession
# ) -> UserMetadata:
#     try:
#         import requests

#         lat, lon = 55.7558, 37.6176  # Москва
#         url = f"https://nominatim.openstreetmap.org/reverse?lat={lat}&lon={lon}&format=json"
#         headers = {"User-Agent": "YourAppName"}
#         response = requests.get(url, headers=headers).json()

#         print(response["address"])

#         user_metadata = UserMetadata(**user_metadata_in.model_dump())

#         session.add(user_metadata)
#         await session.commit()
#         await session.refresh(user_metadata)

#         return user_metadata
#     except Exception as e:
#         raise HTTPException(status_code=400, detail=str(e))
"""==============РЕАЛИЗАЦИЯ С КООРДИНАТАМИ-END========================="""


async def create_user_metadata(
    user_metadata_in: UserMetadataIn, session: AsyncSession
) -> UserMetadata:
    try:
        user_metadata = UserMetadata(**user_metadata_in.model_dump())

        session.add(user_metadata)
        await session.commit()
        await session.refresh(user_metadata)

        return user_metadata
    except IntegrityError:
        raise HTTPException(
            status_code=400, detail="Такого пользователя не существует!"
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


async def get_user_metadata(user_wallet_address: str, session: AsyncSession):
    statement = select(UserMetadata).where(
        UserMetadata.userAddress == user_wallet_address
    )
    result = await session.execute(statement)
    try:
        user_metadata = result.one()
    except NoResultFound:
        raise HTTPException(404, "No user with such wallet_id found")
    except MultipleResultsFound:
        raise HTTPException(500, "Multiple results found, clear the db")
    return user_metadata


async def update_contributed_seconds(
    user_stat_in: UserStatisticsIn, session: AsyncSession
):
    try:
        metadata = await session.get(UserMetadata, user_stat_in.userAddress)
        if not metadata:
            raise HTTPException(status_code=404, detail="User not found")

        metadata.contributedSeconds += user_stat_in.audioLength
        session.add(metadata)
        await session.commit()
        await session.refresh(metadata)
        return metadata
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


async def get_statistics(amount, session: AsyncSession):
    try:
        users = await session.execute(
            select(UserMetadata)
            .order_by(UserMetadata.contributedSeconds.desc()) # type: ignore
            .limit(amount)
        )
        leaders = users.scalars().all()

        user_amount = await session.execute(
            select(func.count(UserMetadata.userAddress))
        )
        user_amount = user_amount.scalar()

        second_amount = await session.execute(
            select(func.sum(UserMetadata.contributedSeconds))
        )
        second_amount = second_amount.scalar()

        return StatisticsOut(
            totalUsers=user_amount,
            totalSeconds=second_amount,
            leaders=Leaders(
                leaders=[
                    Leader(
                        userAddress=leader.userAddress,
                        contributedSeconds=leader.contributedSeconds,
                    )
                    for leader in leaders
                ]
            ),
        )

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


async def create_email(user_email: str, session: AsyncSession):
    try:
        email = Emails(email=user_email)

        session.add(email)
        await session.commit()
        await session.refresh(email)

        return email
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
