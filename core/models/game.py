from enum import StrEnum

from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base


class GameStatusEnum(StrEnum):
    playing = "playing"
    completed = "completed"


class Game(Base):
    name: Mapped[str] = mapped_column(String(32), unique=True)
    room_id: Mapped[id] = mapped_column(ForeignKey("rooms.id"))
    status: Mapped[GameStatusEnum] = mapped_column(default=GameStatusEnum.playing)

    room: Mapped["Room"] = relationship(back_populates="games", lazy="selectin", uselist=False)
    decks: Mapped[list["Room"]] = relationship(back_populates="game", lazy="selectin", uselist=False)
    rounds: Mapped[list["Round"]] = relationship(back_populates="game", lazy="selectin", uselist=False)

    def __str__(self):
        return f"{self.__class__.__name__}(id={self.id}, name={self.name!r})"

    def __repr__(self):
        return str(self)
