import uuid
from uuid import UUID

from pydantic import BaseModel, ConfigDict


class GamesQueryParameters(BaseModel):
    name: str


class GameBase(BaseModel):
    name: str


class GameCreate(GameBase):
    room_id: int


class GameUpdate(GameCreate):
    status: str


class GameUpdatePartial(GameUpdate):
    name: str | None = None


class GameRoom(BaseModel):
    id: int
    name: str


class Game(GameBase):
    model_config = ConfigDict(from_attributes=True)
    id: int
    status: str
    room: GameRoom
