import uuid
from uuid import UUID

from pydantic import BaseModel, ConfigDict


class GameBase(BaseModel):
    name: str
    status: str


class GameCreate(GameBase):
    room_id: int


class GameUpdate(GameCreate):
    pass


class GameUpdatePartial(GameCreate):
    name: str | None = None


class GameRoom(BaseModel):
    id: int
    name: str


class Game(GameBase):
    model_config = ConfigDict(from_attributes=True)
    id: int
    room: GameRoom
