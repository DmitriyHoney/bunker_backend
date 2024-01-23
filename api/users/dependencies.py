from typing import Annotated

from fastapi import Path, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from auth.utils import get_auth_user
from core.models import db_helper, Room, User

from . import crud


async def get_user_by_id(
        room_id: Annotated[int, Path],
        session: AsyncSession = Depends(db_helper.scoped_session_dependency),
) -> Room:
    product = await crud.get_user(session=session, user_id=room_id)
    if product is not None:
        return product

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Product {room_id} not found!",
    )


CurrentUser = Annotated[User | None, Depends(get_auth_user)]
