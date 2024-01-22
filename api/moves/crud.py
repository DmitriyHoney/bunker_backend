"""
Create
Read
Update
Delete
"""

from sqlalchemy import select
from sqlalchemy.engine import Result, ScalarResult
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload, joinedload

from core.models import Move, User, Round, Card, CardProperty

from .schemas import MoveCreate, MoveUpdate, MoveUpdatePartial
from ..games.crud import get_game


async def get_moves(session: AsyncSession) -> list[Move]:
    stmt = select(Move).options(joinedload(Move.card).selectinload(Card.properties)).order_by(Move.id)
    result: ScalarResult = await session.scalars(stmt)
    return result.all()


async def get_move(session: AsyncSession, move_id: int) -> Move | None:
    result = select(Move).where(Move.id == move_id).options(joinedload(Move.card).selectinload(Card.properties))
    return await session.scalar(result)


async def create_move(session: AsyncSession, move_in: MoveCreate) -> Move:
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


async def add_card_to_move(
    session: AsyncSession,
    move: Move,
    card: Card,
) -> Move:
    setattr(move, "card", card)
    await session.commit()
    return move


async def delete_move(
    session: AsyncSession,
    move: Move,
) -> None:
    await session.delete(move)
    await session.commit()
