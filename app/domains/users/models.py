from datetime import datetime
from typing import Optional

from sqlmodel import Field, Relationship, SQLModel


class User(SQLModel, table=True):
    __tablename__ = "users"

    address: str = Field(primary_key=True, index=True, unique=True)
    chainId: str = Field(default="")
    connectedAt: datetime = Field(default_factory=datetime.now)
    lastActivity: datetime = Field(default_factory=datetime.now)
    violations: int = Field(default=0)

    user_metadata: Optional["UserMetadata"] = Relationship(back_populates="user")


class UserMetadata(SQLModel, table=True):
    __tablename__ = "user_metadata"

    id: int = Field(default=None, primary_key=True)
    userAddress: str = Field(default=None, foreign_key="users.address")
    country: str = Field(default="")
    birthMonth: str = Field(default="")
    birthYear: str = Field(default="")
    isItRelated: bool = Field(default=False)
    submittedAt: datetime = Field(default_factory=datetime.now)

    user: User = Relationship(back_populates="user_metadata")

# Used by PoC
class Fingerprints(SQLModel, table=True):
    # The id must be None because it's set by db automatically
    id: int | None = Field(default=None, primary_key=True)
    fprint: bytes
    duration: float
