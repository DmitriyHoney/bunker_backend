"""
Create
Read
Update
Delete
"""

from sqlalchemy import select
from sqlalchemy.engine import Result
from sqlalchemy.ext.asyncio import AsyncSession


from core.models import Game

from .schemas import GameCreate, GameUpdate, GameUpdatePartial


async def get_games(session: AsyncSession) -> list[Game]:
    stmt = select(Game).order_by(Game.id)
    result: Result = await session.execute(stmt)
    rooms = result.scalars().all()
    return list(rooms)


async def get_game(session: AsyncSession, room_id: int) -> Game | None:
    return await session.get(Game, room_id)


async def create_game(session: AsyncSession, user_in: GameCreate) -> Game:
    room = Game(**user_in.model_dump())
    session.add(room)
    await session.commit()
    # await session.refresh(room)
    return room


async def update_game(
    session: AsyncSession,
    room: Game,
    room_update: GameUpdate | GameUpdatePartial,
    partial: bool = False,
) -> Game:
    for name, value in room_update.model_dump(exclude_unset=partial).items():
        setattr(room, name, value)
    await session.commit()
    return room


async def delete_game(
    session: AsyncSession,
    room: Game,
) -> None:
    await session.delete(room)
    await session.commit()