import uuid
from uuid import UUID

from pydantic import BaseModel, ConfigDict


class MovesBase(BaseModel):
    name: str


class MovesCreate(MovesBase):
    room_id: int


class MoveUpdate(MovesCreate):
    pass


class MoveUpdatePartial(MovesCreate):
    name: str | None = None


class Move(MovesBase):
    model_config = ConfigDict(from_attributes=True)
    id: int
