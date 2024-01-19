"""
Create
Read
Update
Delete
"""

from sqlalchemy import select
from sqlalchemy.engine import Result
from sqlalchemy.ext.asyncio import AsyncSession


from core.models import Move, User, Round

from .schemas import MovesCreate, MoveUpdate, MoveUpdatePartial
from ..games.crud import get_game


async def get_moves(session: AsyncSession) -> list[Move]:
    stmt = select(Move).order_by(Move.id)
    result: Result = await session.execute(stmt)
    moves = result.scalars().all()
    return list(moves)


async def get_move(session: AsyncSession, move_id: int) -> Move | None:
    return await session.get(Move, move_id)


async def create_move(session: AsyncSession, move_in: MovesCreate) -> Move:
    move = Move(**move_in.model_dump())
    session.add(move)
    await session.commit()
    # await session.refresh(room)
    return move


async def create_moves(session: AsyncSession, game_id: int) -> list[Move]:
    game = await get_game(session, game_id)

    users = game.room.users

    for r in game.rounds:
        if r.number % 2 != 0:
            users = users.reverse()
        moves = []
        for u in users:
            move = Move()
            move.user = u
            move.round = r
            moves.append(move)
        r.moves = moves

    await session.commit()
    await session.refresh(game.rounds)
    return game.rounds


async def update_move(
    session: AsyncSession,
    move: Move,
    move_update: MoveUpdate | MoveUpdatePartial,
    partial: bool = False,
) -> Move:
    for name, value in move_update.model_dump(exclude_unset=partial).items():
        setattr(move, name, value)
    await session.commit()
    return move


async def delete_move(
    session: AsyncSession,
    move: Move,
) -> None:
    await session.delete(move)
    await session.commit()