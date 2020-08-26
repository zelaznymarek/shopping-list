from typing import Optional

from pydantic import BaseModel


class User(BaseModel):
    email: Optional[str]
    username: str
    is_admin: bool


class UserInDB(User):
    hashed_password: str
