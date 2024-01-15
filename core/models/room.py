import uuid
from sqlalchemy import String, UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship, DynamicMapped

from .base import Base


class Room(Base):
    name: Mapped[str] = mapped_column(String(32), unique=True)
    uid: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), unique=True, default=uuid.uuid4)

    users: Mapped[list["User"]] = relationship(back_populates="room", lazy="selectin")
    games: Mapped[list["Game"]] = relationship(back_populates="room", lazy="selectin")


    def __str__(self):
        return f"{self.__class__.__name__}(id={self.id}, name={self.name!r})"

    def __repr__(self):
        return str(self)
