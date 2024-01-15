import uuid
from enum import StrEnum

from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from .base import Base


class CardApplyEnum(StrEnum):
    none = "none"
    all = "all"
    self = "self"
    one = "one"


class CardEffectEnum(StrEnum):
    none = "none"


class CardProperty(Base):
    name: Mapped[str] = mapped_column(String(128), unique=True)
    value: Mapped[str] = mapped_column(String(128), unique=False)
    description: Mapped[str]
    card_id: Mapped[id] = mapped_column(ForeignKey("cards.id"))
    apply: Mapped[str] = mapped_column(
        CardApplyEnum, nullable=False, default=CardApplyEnum.none
    )
    effect: Mapped[str] = mapped_column(
        CardEffectEnum, nullable=False, default=CardEffectEnum.none
    )

    def __str__(self):
        return f"{self.__class__.__name__}(id={self.id}, name={self.name!r})"

    def __repr__(self):
        return str(self)
