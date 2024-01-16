"""
Create
Read
Update
Delete
"""
from builtins import len

from ..cards.crud import get_random_cards_deck
from ..decks.crud import create_deck

from sqlalchemy import select
from sqlalchemy.engine import Result
from sqlalchemy.ext.asyncio import AsyncSession


from core.models import Game, Deck

from .schemas import GameCreate, GameUpdate, GameUpdatePartial
from ..decks.schemas import DeckCreate


async def get_games(session: AsyncSession) -> list[Game]:
    stmt = select(Game).order_by(Game.id)
    result: Result = await session.execute(stmt)
    rooms = result.scalars().all()
    return list(rooms)


async def get_game(session: AsyncSession, game_id: int) -> Game | None:
    return await session.get(Game, game_id)


async def create_game(session: AsyncSession, game_in: GameCreate) -> Game:
    game = Game(**game_in.model_dump())
    session.add(game)
    await session.flush()
    await session.refresh(game)

    users = game.room.users
    random_decks = get_random_cards_deck(session=session, limit=len(users))

    for user in game.room.users:
        deck = Deck(game_id=game.id, )
        session.add(deck)

        await session.commit()
        deck = create_deck(session=session, )

    print(game.room.users)

    await session.commit()

    return game


async def update_game(
    session: AsyncSession,
    game: Game,
    game_update: GameUpdate | GameUpdatePartial,
    partial: bool = False,
) -> Game:
    for name, value in game_update.model_dump(exclude_unset=partial).items():
        setattr(game, name, value)
    await session.commit()
    return game


async def delete_game(
    session: AsyncSession,
    game: Game,
) -> None:
    await session.delete(game)
    await session.commit()
