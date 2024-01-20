import uuid
from uuid import UUID

from pydantic import BaseModel, ConfigDict

from core.models import CardCategoryEnum
from core.models.card_property import CardApplyEnum, CardEffectEnum


class MovesBase(BaseModel):
    pass


class MovesCreate(MovesBase):
    game_id: int


class MoveUpdate(MovesCreate):
    pass


class MoveUpdatePartial(MovesCreate):
    name: str | None = None


class MoveCardProperty(BaseModel):
    name: str
    value: str
    description: str
    apply: CardApplyEnum
    effect: CardEffectEnum


class MoveCard(BaseModel):
    name: str
    description: str
    category: CardCategoryEnum
    effect: float
    properties: list[MoveCardProperty] = []


class MoveResponse(MovesBase):
    id: int
    card: MoveCard | None

    model_config = ConfigDict(from_attributes=True)