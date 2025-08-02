from datetime import datetime

from pydantic import BaseModel


class UserIn(BaseModel):
    address: str
    chainId: str


class UserMetadataIn(BaseModel):
    userAddress: str
    country: str
    birthMonth: str
    birthYear: str
    isItRelated: bool
