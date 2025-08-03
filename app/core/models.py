from datetime import datetime

from sqlmodel import Field, SQLModel


class UserIn(SQLModel):
    wallet_address: str
    country: str
    birth_month: int = Field(ge=1, le=12)
    birth_year: int = Field(ge=1900)


class Users(SQLModel, table=True):
    wallet_address: str = Field(primary_key=True)
    country: str
    birth_month: int = Field(ge=1, le=12)
    birth_year: int = Field(ge=1900)
    submitted_at: datetime = Field(default_factory=datetime.now)
    connected_at: datetime = Field(default_factory=datetime.now)
    last_activity: datetime = Field(default_factory=datetime.now)


# Used by PoC
class Fingerprints(SQLModel, table=True):
    # The id must be None because it's set by db automatically
    id: int | None = Field(default=None, primary_key=True)
    fprint: bytes
    duration: float
