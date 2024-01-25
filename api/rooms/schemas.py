import uuid

from typing import TYPE_CHECKING
from pydantic import BaseModel, ConfigDict


from api.users.schemas import User
from core.models import GameStatusEnum


class RoomBase(BaseModel):
    name: str


class RoomCreate(RoomBase):
    username: str


class RoomUpdate(RoomCreate):
    pass


class RoomUpdatePartial(RoomCreate):
    name: str | None = None


class RoomUser(BaseModel):
    id: int
    uid: uuid.UUID
    username: str
    is_owner: bool


class RoomGame(BaseModel):
    id: int
    name: str
    status: GameStatusEnum


class Room(RoomBase):
    model_config = ConfigDict(from_attributes=True)
    id: int
    uid: uuid.UUID
    users: list[RoomUser] = []
    games: list[RoomGame] = []
