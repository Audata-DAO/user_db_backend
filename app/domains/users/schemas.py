from datetime import datetime

from pydantic import BaseModel
from sqlmodel import Field


class UserIn(BaseModel):
    address: str
    chainId: str


class UserMetadataIn(BaseModel):
    userAddress: str
    countryCode: str
    country: str
    birthMonth: str
    birthYear: str
    isItRelated: bool
    region: str


class UserStatisticsIn(BaseModel):
    userAddress: str
    audioLength: float = Field(gt=0.0)
