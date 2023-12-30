import uuid

from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from .base import Base


class CardSpecification(Base):
    name: Mapped[str] = mapped_column(String(128), unique=True)
    value: Mapped[str] = mapped_column(String(128), unique=False)
    description: Mapped[str]
    card_id: Mapped[id] = mapped_column(ForeignKey("cards.id"))

    def __str__(self):
        return f"{self.__class__.__name__}(id={self.id}, name={self.name!r})"

    def __repr__(self):
        return str(self)
