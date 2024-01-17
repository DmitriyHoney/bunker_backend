"""
Create
Read
Update
Delete
"""
from builtins import len

from ..cards.crud import get_random_cards_deck
from sqlalchemy import select
from sqlalchemy.engine import Result
from sqlalchemy.ext.asyncio import AsyncSession


from core.models import Game, Deck, Round

from .schemas import GameCreate, GameUpdate, GameUpdatePartial
from ..decks.schemas import DeckCreate


async def get_games(session: AsyncSession) -> list[Game]:
    stmt = select(Game).order_by(Game.id)
    result: Result = await session.execute(stmt)
    rooms = result.scalars().all()
    return list(rooms)


async def get_game(session: AsyncSession, game_id: int) -> Game | None:
    return await session.get(Game, game_id)


async def create_rounds(session: AsyncSession, game: Game) -> list[Round]:
    rounds = []
    for i in range(9):
        round = Round(name=f"round_{i + 1}")
        round.game = game
        session.add(round)
        rounds.append(round)
    await session.commit()
    return rounds


async def create_game(session: AsyncSession, game_in: GameCreate) -> Game:
    game = Game(**game_in.model_dump())
    session.add(game)
    # await session.flush()
    # await session.refresh(game)
    #
    # users = game.room.users
    # random_decks = await get_random_cards_deck(session=session, limit=len(users))
    #
    # for i, user in enumerate(game.room.users):
    #     deck = Deck()
    #     deck.game = game
    #     deck.user = user
    #     deck.cards = random_decks[i]
    #     session.add(deck)
    #
    # create_rounds(game)
    #
    # for i in range(9):
    #     round = Round(name=f"round_{i + 1}")

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


