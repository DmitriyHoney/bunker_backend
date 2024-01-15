"""
Create
Read
Update
Delete
"""

from sqlalchemy import select
from sqlalchemy.engine import Result
from sqlalchemy.ext.asyncio import AsyncSession


from core.models import Deck

from .schemas import DeckCreate, DeckUpdate, DeckUpdatePartial


async def get_decks(session: AsyncSession) -> list[Deck]:
    stmt = select(Deck).order_by(Deck.id)
    result: Result = await session.execute(stmt)
    rooms = result.scalars().all()
    return list(rooms)


async def get_deck(session: AsyncSession, deck_id: int) -> Deck | None:
    return await session.get(Deck, deck_id)


async def create_deck(session: AsyncSession, deck_in: DeckCreate) -> Deck:
    deck = Deck(**deck_in.model_dump())
    session.add(deck)
    await session.commit()
    # await session.refresh(room)
    return deck


async def update_deck(
    session: AsyncSession,
    deck: Deck,
    deck_update: DeckUpdate | DeckUpdatePartial,
    partial: bool = False,
) -> Deck:
    for name, value in deck_update.model_dump(exclude_unset=partial).items():
        setattr(deck, name, value)
    await session.commit()
    return deck


async def delete_deck(
    session: AsyncSession,
    deck: Deck,
) -> None:
    await session.delete(deck)
    await session.commit()
