from enum import Enum

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base

class CardCategoryEnum(Enum):
    health = "health"
    profession = "profession"
    phobia = "phobia"
    hobby = "hobby"
    luggage = "luggage"
    quality = "quality"
    special = "special"
    biology = "biology"
    skill = "skill"
    bunker = "bunker"
    disaster = "disaster"


card_categories = [category.name for category in CardCategoryEnum] + [CardCategoryEnum.special]


class Card(Base):
    name: Mapped[str] = mapped_column(String(128), unique=True)
    description: Mapped[str]
    category: Mapped[CardCategoryEnum] = mapped_column(nullable=False, default=CardCategoryEnum.special)
    effect: Mapped[float] = mapped_column(default=0.5)

    properties: Mapped[list["CardProperty"]] = relationship(back_populates="card", uselist=True)
    decks: Mapped[list["Deck"]] = relationship(back_populates="cards", uselist=True, secondary='card_deck')
    moves: Mapped[list["Move"]] = relationship(back_populates="card", uselist=True)

    def __str__(self):
        return f"{self.__class__.__name__}(id={self.id}, name={self.name!r})"

    def __repr__(self):
        return str(self)
