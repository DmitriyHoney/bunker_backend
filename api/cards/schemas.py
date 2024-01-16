from pydantic import BaseModel, ConfigDict

from core.models import CardCategoryEnum


class CardBase(BaseModel):
    name: str
    description: str
    effect: int
    category: CardCategoryEnum


class CardCreate(CardBase):
    pass


class CardUpdate(CardCreate):
    pass


class CardUpdatePartial(CardCreate):
    name: str | None = None
    description: str | None = None
    effect: int | None = None


class Card(CardBase):
    model_config = ConfigDict(from_attributes=True)
    id: int


class CardSet(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    category: CardCategoryEnum
    cards: list[Card]


