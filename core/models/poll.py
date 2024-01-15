from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base


class Poll(Base):
    round_id: Mapped[int] = mapped_column(ForeignKey("rounds.id"))

    round: Mapped["Round"] = relationship(back_populates="polls", lazy="selectin", uselist=False)
    voices: Mapped[list["Voice"]] = relationship(back_populates="poll", lazy="selectin", uselist=True)

    def __str__(self):
        return f"{self.__class__.__name__}(id={self.id}, name={self.id!r})"

    def __repr__(self):
        return str(self)
