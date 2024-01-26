from typing import Annotated

from fastapi import Path, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from core import exceptions
from core.models import db_helper, Move

from . import crud


async def get_move_by_id(
    move_id: Annotated[int, Path],
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
) -> Move:
    move = await crud.get_move(session=session, move_id=move_id)
    if move is not None:
        return move

    raise exceptions.APIException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Ход {move_id} не найден!",
    )
