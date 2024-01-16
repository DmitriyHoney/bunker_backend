
from pydantic import BaseModel, ConfigDict

from core.models import CardCategoryEnum, GameStatusEnum


class DeckBase(BaseModel):
    pass


class DeckCreate(DeckBase):
    room_id: int


class DeckUpdate(DeckCreate):
    pass


class DeckUpdatePartial(DeckCreate):
    name: str | None = None


class DeckCards(BaseModel):
    id: int
    name: str
    description: str
    effect: int
    category: CardCategoryEnum


class DeckUser(BaseModel):
    id: int
    username: str


class DeckGame(BaseModel):
    id: int
    name: str
    status: GameStatusEnum


class Deck(DeckBase):
    model_config = ConfigDict(from_attributes=True)
    id: int
    cards: list[DeckCards] = []
    user: DeckUser
    game: DeckGame
