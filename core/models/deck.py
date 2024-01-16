from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base


class CardDeck(Base):
    __tablename__ = 'card_deck'

    card_id: Mapped[int] = mapped_column(ForeignKey("cards.id"))
    deck_id: Mapped[int] = mapped_column(ForeignKey("decks.id"))


class Deck(Base):
    game_id: Mapped[int] = mapped_column(ForeignKey("games.id", ondelete='all, delete'))
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))

    cards: Mapped[list["Card"]] = relationship(secondary="card_deck", uselist=True, lazy="selectin",
                                               back_populates="decks")
    user: Mapped["User"] = relationship(back_populates="decks", lazy="selectin", uselist=False)
    game: Mapped["Game"] = relationship(back_populates="decks", lazy="selectin", uselist=False)

    def __str__(self):
        return f"{self.__class__.__name__}(id={self.id}, name={self.user_id!r})"

    def __repr__(self):
        return str(self)
