"""
Create
Read
Update
Delete
"""

from sqlalchemy import select
from sqlalchemy.engine import Result
from sqlalchemy.ext.asyncio import AsyncSession

from core.models import Game, Round
from .schemas import RoundCreate, RoundUpdate, RoundUpdatePartial


async def get_rounds(session: AsyncSession) -> list[Game]:
    stmt = select(Round).order_by(Round.id)
    result: Result = await session.execute(stmt)
    rounds = result.scalars().all()
    return list(rounds)


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

async def create_rounds(session: AsyncSession, round_in: RoundCreate) -> list[Round]:
    all_rounds = []
    for i in range(8):
        round_name = f"Раунд {i + 1}"
        all_rounds.append(Round(name=round_name, **round_in.model_dump()))
    session.add_all(all_rounds)
    await session.commit()
    return all_rounds



async def update_game(
    session: AsyncSession,
    game: Game,
    game_update: RoundUpdate | RoundUpdatePartial,
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


