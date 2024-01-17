import enum

from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base


class RoundStatusEnum(enum.Enum):
    waiting = "waiting"
    playing = "playing"
    played = "played"

# class RoundStatusEnum(enum.Enum):
#     waiting = "waiting"
#     playing = "playing"
#     played = "played"


class Round(Base):

    name: Mapped[str] = mapped_column(String(32))
    game_id: Mapped[int] = mapped_column(ForeignKey("games.id"))
    #status: Mapped[RoundStatusEnum] = mapped_column(nullable=False, default="waiting")

    game: Mapped["Game"] = relationship(back_populates="rounds", lazy="selectin", uselist=False)
    polls: Mapped[list["Poll"]] = relationship(back_populates="round", lazy="selectin", uselist=True)
    moves: Mapped[list["Move"]] = relationship(back_populates="round", lazy="selectin", uselist=True)

    def __str__(self):
        return f"{self.__class__.__name__}(id={self.id}, name={self.name!r})"

    def __repr__(self):
        return str(self)
