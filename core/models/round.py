import uuid

from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from .base import Base


class Round(Base):
    name: Mapped[str] = mapped_column(String(32), unique=True)
    game_id: Mapped[int] = mapped_column(ForeignKey('games.id'))

    #uid: Mapped[uuid] = mapped_column(unique=True, default_factory=uuid.uuid4)

    def __str__(self):
        return f"{self.__class__.__name__}(id={self.id}, name={self.name!r})"

    def __repr__(self):
        return str(self)
