import uuid

from pydantic import BaseModel, ConfigDict

from api.auth.schemas import Token


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
    # room: object | None
    # moves: list | None
    # votes: list | None
    # exclude_votes: list | None


class UserCreateResponse(User):
    model_config = ConfigDict(from_attributes=True)
    id: int
    uid: uuid.UUID
    token: Token





