from typing import Annotated

from fastapi import Path, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from core.models import db_helper, Room

from . import crud


async def get_room_by_id(
    room_id: Annotated[int, Path],
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
) -> Room:
    room = await crud.get_room(session=session, room_id=room_id)
    if room is not None:
        return room

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Room {room_id} not found!",
    )
