from typing import Annotated

from fastapi import Path, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from core.exceptions import APIException
from core.models import db_helper, Room, User

from . import crud


async def get_user_by_id(
        user_id: Annotated[int, Path],
        session: AsyncSession = Depends(db_helper.scoped_session_dependency),
) -> User:
    user = await crud.get_user(session=session, user_id=user_id)
    if user is not None:
        return user

    raise APIException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"User {user_id} not found!",
    )



