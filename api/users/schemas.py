import uuid
from uuid import UUID

from pydantic import BaseModel, ConfigDict


class UserBase(BaseModel):
    username: str
    is_owner: bool = False


class UserCreate(UserBase):
    room_id: int


class UserUpdate(UserCreate):
    pass


class UserUpdatePartial(UserCreate):
    name: str | None = None


class User(UserBase):
    model_config = ConfigDict(from_attributes=True)
    id: int
    uid: uuid.UUID
