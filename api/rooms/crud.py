"""
Create
Read
Update
Delete
"""
import uuid

from sqlalchemy import select
from sqlalchemy.engine import Result, ScalarResult
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from core.models import Room, User

from .schemas import RoomCreate, RoomUpdate, RoomUpdatePartial


async def get_rooms(session: AsyncSession, user_id: int | None) -> list[Room]:
    query = select(Room).order_by(Room.id)
    if user_id is not None:
        query = query.join(User).where(User.id == user_id)

    result: ScalarResult = await session.scalars(query)
    #rooms = result.scalars().all()
    return result.all()


async def get_room(session: AsyncSession, room_id: int) -> Room | None:
    return await session.get(Room, room_id)


async def get_room_by_user(session: AsyncSession, user_id: int) -> Room | None:
    query = select(Room).join(User).filter(User.id == user_id)
    return await session.scalar(query)


async def create_room(session: AsyncSession, room_in: RoomCreate) -> Room:

    request_data = room_in.model_dump()
    owner_username = request_data.pop("username")
    room = Room(**request_data)
    owner = User(is_owner=True, username=owner_username)
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
