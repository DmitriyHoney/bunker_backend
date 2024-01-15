from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base


class Vote(Base):
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    poll_id: Mapped[int] = mapped_column(ForeignKey("polls.id"))
    exclude_user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))

    poll: Mapped["Poll"] = relationship(back_populates="votes", lazy="selectin", uselist=False)
    user: Mapped["User"] = relationship(back_populates="votes", lazy="selectin", uselist=False)
    exclude_user: Mapped["User"] = relationship(back_populates="exclude_votes", lazy="selectin", uselist=False)

    def __str__(self):
        return f"{self.__class__.__name__}(id={self.id}, name={self.id!r})"

    def __repr__(self):
        return str(self)
