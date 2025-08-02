from fastapi import HTTPException
from sqlalchemy.exc import IntegrityError
from sqlmodel.ext.asyncio.session import AsyncSession

from app.domains.users.models import User, UserMetadata
from app.domains.users.schemas import UserIn, UserMetadataIn


async def create_user(user_in: UserIn, session: AsyncSession) -> User:
    try:
        user = User(**user_in.model_dump())

        session.add(user)
        await session.commit()
        await session.refresh(user)

        return user
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


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


async def create_user_metadata(user_metadata_in: UserMetadataIn, session: AsyncSession) -> UserMetadata:
    try:
        user_metadata = UserMetadata(**user_metadata_in.model_dump())

        session.add(user_metadata)
        await session.commit()
        await session.refresh(user_metadata)

        return user_metadata
    except IntegrityError:
        raise HTTPException(status_code=400, detail="Такого пользователя не существует!")
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
