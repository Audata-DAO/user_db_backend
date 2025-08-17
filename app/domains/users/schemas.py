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


class Leader(BaseModel):
    userAddress: str
    contributedSeconds: float


class Leaders(BaseModel):
    leaders: list[Leader]


class StatisticsOut(BaseModel):
    totalUsers: int
    totalSeconds: float
    leaders: Leaders
