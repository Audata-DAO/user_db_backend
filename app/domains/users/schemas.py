from sqlmodel import Field, SQLModel


class UserIn(SQLModel):
    wallet_address: str
    country: str
    birth_month: int = Field(ge=1, le=12)
    birth_year: int = Field(ge=1900)
