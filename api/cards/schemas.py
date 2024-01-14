from pydantic import BaseModel, ConfigDict


class CardBase(BaseModel):
    name: str
    description: str
    price: int


class CardCreate(CardBase):
    pass


class CardUpdate(CardCreate):
    pass


class CardUpdatePartial(CardCreate):
    name: str | None = None
    description: str | None = None
    price: int | None = None


class Card(CardBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
