from pydantic import BaseModel


class UserIn(BaseModel):
    address: str
    chainId: str
