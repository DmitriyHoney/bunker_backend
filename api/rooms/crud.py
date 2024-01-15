"""
Create
Read
Update
Delete
"""
import uuid

from sqlalchemy import select
from sqlalchemy.engine import Result
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from core.models import Room, User

from .schemas import RoomCreate, RoomUpdate, RoomUpdatePartial


async def get_rooms(session: AsyncSession) -> list[Room]:
    stmt = select(Room).order_by(Room.id)
    result: Result = await session.execute(stmt)
    rooms = result.scalars().all()
    return list(rooms)


async def get_room(session: AsyncSession, room_id: int) -> Room | None:
    return await session.get(Room, room_id)


async def get_room_by_user(session: AsyncSession, user_id: int) -> Room | None:

    print("ddddddddddddddd", user_id)

    stmt = select(Room).where(Room.users.and_(User.id == user_id))

    print(stmt)

    result = await session.execute(stmt)

    return result.scalars().one()


async def create_room(session: AsyncSession, room_in: RoomCreate) -> Room:
    room = Room(**room_in.model_dump())
    owner = User(is_owner=True, username=uuid.uuid4().hex)
    room.users.append(owner)
    session.add(room)
    await session.commit()
    await session.refresh(room)
    return room


async def update_room(
    session: AsyncSession,
    room: Room,
    room_update: RoomUpdate | RoomUpdatePartial,
    partial: bool = False,
) -> Room:
    for name, value in room_update.model_dump(exclude_unset=partial).items():
        setattr(room, name, value)
    await session.commit()
    return room


async def delete_room(
    session: AsyncSession,
    room: Room,
) -> None:
    await session.delete(room)
    await session.commit()
