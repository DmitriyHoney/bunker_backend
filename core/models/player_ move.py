import uuid
from typing import TYPE_CHECKING
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base

if TYPE_CHECKING:
    from .user import User
    from .card import Card


class PlayerMove(Base):
    __tablename__ = "player_moves"

    round_id: Mapped[int] = mapped_column(ForeignKey("rounds.id"))
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    card_id: Mapped[int] = mapped_column(ForeignKey("cards.id"))

    user = Mapped["User"] = relationship(back_populates='player_moves')
    card = Mapped["Card"] = relationship(back_populates='player_moves')

    def __str__(self):
        return f"{self.__class__.__name__}(id={self.id}, name={self.name!r})"

    def __repr__(self):
        return str(self)
