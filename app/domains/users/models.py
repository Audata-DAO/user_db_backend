from datetime import datetime
from typing import Optional

from sqlmodel import Field, Relationship, SQLModel


class User(SQLModel, table=True):
    __tablename__ = "users"

    address: str = Field(primary_key=True, index=True, unique=True)
    chainId: str
    connectedAt: datetime = Field(default_factory=datetime.now)
    lastActivity: datetime = Field(default_factory=datetime.now)
    violations: int = 0

    user_metadata: Optional["UserMetadata"] = Relationship(back_populates="user")


class UserMetadata(SQLModel, table=True):
    __tablename__ = "user_metadata"

    userAddress: str = Field(default=None, foreign_key="users.address", primary_key=True)
    countryCode: str
    country: str
    region: str
    birthMonth: str
    birthYear: str
    isItRelated: bool = False
    contributedSeconds: float = Field(default=0)
    submittedAt: datetime = Field(default_factory=datetime.now)

    user: User = Relationship(back_populates="user_metadata")


# Used by PoC
class Fingerprints(SQLModel, table=True):
    # The id must be None because it's set by db automatically
    id: int | None = Field(default=None, primary_key=True)
    fprint: bytes
    duration: float
