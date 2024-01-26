"""
Create
Read
Update
Delete
"""
import datetime
import uuid

from sqlalchemy import select
from sqlalchemy.engine import Result
from sqlalchemy.ext.asyncio import AsyncSession

from core import exceptions
from core.exceptions import APIException
from core.models import Game, Round, RoundStateEnum, Move
from .schemas import RoundUpdate, RoundUpdatePartial


async def get_rounds(session: AsyncSession) -> list[Game]:
    stmt = select(Round).order_by(Round.id)
    result: Result = await session.execute(stmt)
    rounds = result.scalars().all()
    return list(rounds)


async def get_game(session: AsyncSession, game_id: int) -> Game | None:
    return await session.get(Game, game_id)


async def create_rounds(session: AsyncSession, game_id: int) -> list[Round]:
    all_rounds = []
    game = await get_game(session, game_id)

    if len(game.rounds):
        raise exceptions.APIException(detail=f"Игра {game.id} уже содержит раунды")

    if not hasattr(game, 'room'):
        raise APIException(detail="Комната не найдена")

    users = game.room.users

    for i in range(8):
        round_name = f"Раунд {i + 1}"
        if i + 1 % 2 != 0:
            users = list(reversed(users))
        moves = []
        for y, u in enumerate(users):
            move = Move(user=u)
            if y == 0 and i == 0:
                move.expired_date = datetime.datetime.utcnow() + datetime.timedelta(minutes=5)
            moves.append(move)

        all_rounds.append(Round(
            name=round_name,
            number=i + 1,
            state=RoundStateEnum.playing if i == 0 else RoundStateEnum.waiting,
            game=game,
            moves=moves
        ))

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


