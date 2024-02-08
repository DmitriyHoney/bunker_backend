from enum import Enum

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base


class PollStatusEnum(Enum):
    open = 'open'
    close = 'close'


class Poll(Base):
    round_id: Mapped[int] = mapped_column(ForeignKey("rounds.id"))
    status: Mapped[PollStatusEnum] = mapped_column(default=PollStatusEnum.open)

    round: Mapped["Round"] = relationship(back_populates="polls", lazy="selectin", uselist=False)
    votes: Mapped[list["Vote"]] = relationship(back_populates="poll", lazy="selectin", uselist=True)

    def __str__(self):
        return f"{self.__class__.__name__}(id={self.id}, name={self.id!r})"

    def __repr__(self):
        return str(self)
