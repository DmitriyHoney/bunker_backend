import uuid

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from .base import Base


class Room(Base):
    name: Mapped[str] = mapped_column(String(32), unique=True)
    #uid: Mapped[uuid] = mapped_column(unique=True, default_factory=uuid.uuid4)

    def __str__(self):
        return f"{self.__class__.__name__}(id={self.id}, name={self.name!r})"

    def __repr__(self):
        return str(self)
