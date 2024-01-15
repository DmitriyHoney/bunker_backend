import uuid
from enum import Enum

from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base


class CardApplyEnum(Enum):
    none = "none"
    all = "all"
    self = "self"
    one = "one"


class CardEffectEnum(Enum):
    none = "none"


class CardProperty(Base):
    name: Mapped[str] = mapped_column(String(128), unique=True)
    value: Mapped[str] = mapped_column(String(128), unique=False)
    description: Mapped[str]
    card_id: Mapped[id] = mapped_column(ForeignKey("cards.id"))
    apply: Mapped[CardApplyEnum] = mapped_column(nullable=False, default=CardApplyEnum.none)
    effect: Mapped[CardEffectEnum] = mapped_column(nullable=False, default=CardEffectEnum.none)

    card: Mapped["Card"] = relationship(back_populates="properties", lazy="selectin", uselist=False)

    def __str__(self):
        return f"{self.__class__.__name__}(id={self.id}, name={self.name!r})"

    def __repr__(self):
        return str(self)
