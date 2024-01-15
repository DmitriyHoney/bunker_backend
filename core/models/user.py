import uuid

from sqlalchemy import String, ForeignKey, UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base


class User(Base):
    username: Mapped[str] = mapped_column(String(32), unique=True)
    room_id: Mapped[int] = mapped_column(ForeignKey("rooms.id"))
    is_owner: Mapped[bool] = mapped_column(default=False)
    uid: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), unique=True, default=uuid.uuid4
    )
    room: Mapped["Room"] = relationship(back_populates="users")

    def __str__(self):
        return f"{self.__class__.__name__}(id={self.id}, username={self.username!r})"

    def __repr__(self):
        return str(self)
