from datetime import datetime

from sqlmodel import Field, SQLModel


class User(SQLModel, table=True):
    __tablename__ = "users"

    id: int = Field(default=None, primary_key=True)
    address: str = Field(default="", index=True, unique=True)
    chainId: str = Field(default="")
    connectedAt: datetime = Field(default_factory=datetime.now)
    lastActivity: datetime = Field(default_factory=datetime.now)
