"""
Create
Read
Update
Delete
"""

from sqlalchemy import select
from sqlalchemy.engine import Result
from sqlalchemy.ext.asyncio import AsyncSession

from core.config import settings
from core.exceptions import APIException
from core.models import Deck, GameStatusEnum
from core.models.card import card_user_categories

from .schemas import DeckCreate, DeckUpdate, DeckUpdatePartial
from ..cards.crud import get_random_cards_deck
from ..games.crud import get_game


async def get_decks(session: AsyncSession) -> list[Deck]:
    stmt = select(Deck).order_by(Deck.id)
    result: Result = await session.execute(stmt)
    rooms = result.scalars().all()
    return list(rooms)


async def get_deck(session: AsyncSession, deck_id: int) -> Deck | None:

    select(Deck).filt()

    return await session.get(Deck, deck_id)


async def get_deck_by_game_user(session: AsyncSession, game_id: int, user_id: int) -> Deck | None:
    return await session.scalar(select(Deck).where(Deck.user_id == user_id, Deck.game_id == game_id))


async def create_deck(session: AsyncSession, deck_in: DeckCreate) -> Deck:
    deck = Deck(**deck_in.model_dump())
    session.add(deck)

    await session.commit()
    # await session.refresh(room)
    return deck


async def create_decks(session: AsyncSession, deck_in: DeckCreate) -> list[Deck]:
    game = await get_game(session, **deck_in.model_dump())

    if not game:
        raise APIException(detail=f"Игры ID {deck_in.game_id} не существует")

    if game.status == GameStatusEnum.completed:
        raise APIException(detail=f"Игра ID {deck_in.game_id} завершена")

    users = game.room and game.room.users
    random_decks = await get_random_cards_deck(session=session, limit=len(users))

    # if all(True for i in random_decks if len(i) == settings.game.rounds_count):
    #     raise APIException(detail="Колоды игроков не укомплектованы")

    all_deck = []

    for i, user in enumerate(users):
        deck = Deck(game=game, user=user)
        deck.cards = random_decks[i]
        all_deck.append(deck)

    session.add_all(all_deck)
    await session.commit()
    return all_deck


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
