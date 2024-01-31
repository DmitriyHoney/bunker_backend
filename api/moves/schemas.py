from pydantic import BaseModel, ConfigDict
from core.models import CardCategoryEnum
from core.models.card_property import CardApplyEnum, CardEffectEnum


class MoveBase(BaseModel):
    pass


class MoveCreate(MoveBase):
    game_id: int


class MoveUpdate(MoveCreate):
    pass


class MoveUpdatePartial(MoveCreate):
    name: str | None = None


class MoveCardProperty(BaseModel):
    name: str
    value: str
    description: str
    apply: CardApplyEnum
    effect: CardEffectEnum


class MoveCard(BaseModel):
    id: int
    name: str
    description: str
    category: CardCategoryEnum
    effect: float
    properties: list[MoveCardProperty] = []


class MoveResponse(MoveBase):
    id: int
    card: MoveCard | None

    model_config = ConfigDict(from_attributes=True)