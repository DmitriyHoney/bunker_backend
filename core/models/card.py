import uuid
from enum import Enum, StrEnum

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

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


class Card(Base):
    name: Mapped[str] = mapped_column(String(128), unique=True)
    description: Mapped[str]
    category: Mapped[CardCategoryEnum] = mapped_column(nullable=False)
    effect: Mapped[float] = mapped_column(default=0.5)

    def __str__(self):
        return f"{self.__class__.__name__}(id={self.id}, name={self.name!r})"

    def __repr__(self):
        return str(self)
