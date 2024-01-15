import uuid

from typing import TYPE_CHECKING
from pydantic import BaseModel, ConfigDict


from api.users.schemas import User


class RoomBase(BaseModel):
    name: str


class RoomCreate(RoomBase):
    username: str


class RoomUpdate(RoomCreate):
    pass


class RoomUpdatePartial(RoomCreate):
    name: str | None = None


class Room(RoomBase):
    model_config = ConfigDict(from_attributes=True)
    id: int
    uid: uuid.UUID
    users: list[User] = []
