"""
Create
Read
Update
Delete
"""

from sqlalchemy import select
from sqlalchemy.engine import Result
from sqlalchemy.ext.asyncio import AsyncSession


from core.models import User

from .schemas import UserCreate, UserUpdate, UserUpdatePartial




async def get_users(session: AsyncSession) -> list[User]:
    stmt = select(User).order_by(User.id)
    result: Result = await session.execute(stmt)
    rooms = result.scalars().all()
    return list(rooms)


async def get_user(session: AsyncSession, user_id: int) -> User | None:
    return await session.get(User, user_id)


async def create_user(session: AsyncSession, user_in: UserCreate) -> User:
    user = User(**user_in.model_dump())

    session.add(user)
    await session.commit()
    return user


async def update_user(
    session: AsyncSession,
    room: User,
    room_update: UserUpdate | UserUpdatePartial,
    partial: bool = False,
) -> User:
    for name, value in room_update.model_dump(exclude_unset=partial).items():
        setattr(room, name, value)
    await session.commit()
    return room


async def delete_user(
    session: AsyncSession,
    room: User,
) -> None:
    await session.delete(room)
    await session.commit()
