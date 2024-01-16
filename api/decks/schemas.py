
from pydantic import BaseModel, ConfigDict


class DeckBase(BaseModel):
    pass


class DeckCreate(DeckBase):
    room_id: int


class DeckUpdate(DeckCreate):
    pass


class DeckUpdatePartial(DeckCreate):
    name: str | None = None


class Deck(DeckBase):
    model_config = ConfigDict(from_attributes=True)
    id: int

