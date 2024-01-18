import uuid
from enum import Enum

from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base


class RoundStateEnum(Enum):
    waiting = "waiting"
    playing = "playing"
    played = "played"


class Round(Base):
    name: Mapped[str] = mapped_column(String(32), unique=True)
    game_id: Mapped[int] = mapped_column(ForeignKey("games.id"))
    state: Mapped[RoundStateEnum] = mapped_column(nullable=False, default=RoundStateEnum.waiting)
    number: Mapped[int]

    game: Mapped["Game"] = relationship(back_populates="rounds", lazy="selectin", uselist=False)
    polls: Mapped[list["Poll"]] = relationship(back_populates="round", lazy="selectin", uselist=True)
    moves: Mapped[list["Move"]] = relationship(back_populates="round", lazy="selectin", uselist=True)

    def __str__(self):
        return f"{self.__class__.__name__}(id={self.id}, name={self.name!r})"

    def __repr__(self):
        return str(self)
