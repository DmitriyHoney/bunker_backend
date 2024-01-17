import uuid
from uuid import UUID

from pydantic import BaseModel, ConfigDict


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
    id: int
    name: str


class Round(RoundBase):
    model_config = ConfigDict(from_attributes=True)
    id: int
    name: str
    game: RoundGame
