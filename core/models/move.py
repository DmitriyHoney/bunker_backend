import uuid
from datetime import datetime
from typing import TYPE_CHECKING
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base

# if TYPE_CHECKING:
#     from .user import User
#     from .card import Card
#


class Move(Base):
    round_id: Mapped[int] = mapped_column(ForeignKey("rounds.id"))
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    card_id: Mapped[int | None] = mapped_column(ForeignKey("cards.id"), nullable=True)
    expired_date: Mapped[datetime | None]

    user: Mapped["User"] = relationship(back_populates="moves", lazy="selectin", uselist=False)
    card: Mapped["Card"] = relationship(back_populates="moves", lazy="selectin", uselist=False)
    round: Mapped["Round"] = relationship(back_populates="moves", lazy="selectin", uselist=False)

    def __str__(self):
        return f"{self.__class__.__name__}(id={self.id}, name={self.user_id!r})"

    def __repr__(self):
        return str(self)
