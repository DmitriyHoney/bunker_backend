import uuid
from datetime import datetime
from typing import Annotated
from uuid import UUID

from fastapi import Query
from pydantic import BaseModel, ConfigDict

from core.models import RoundStateEnum, GameStatusEnum


class RoundsFilterModel(BaseModel):
    game_id: int | None = None


class RoundBase(BaseModel):
    pass
    #status: str


class RoundCreate(RoundBase):
    game_id: int


class RoundUpdate(RoundCreate):
    pass


class RoundUpdatePartial(RoundCreate):
    name: str | None = None


class RoundGame(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    name: str
    status: GameStatusEnum


class RoundMovesUser(BaseModel):
    id: int
    username: str


class RoundMoves(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    expired_date: datetime | None
    user: RoundMovesUser


class Round(RoundBase):
    model_config = ConfigDict(from_attributes=True)
    id: int
    name: str
    number: int
    state: RoundStateEnum
    game: RoundGame
    moves: list[RoundMoves]
