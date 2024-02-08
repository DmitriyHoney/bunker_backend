from typing import Annotated

from fastapi import Path, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from core import exceptions
from core.models import db_helper, Game

from . import crud


async def rounds_filters(
    game_id: int | None = None
):
    return {'game_id': game_id}


RoundsFilterParams = Annotated[dict, Depends(rounds_filters)]


async def get_poll_by_id(
    poll_id: Annotated[int, Path],
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
) -> Game:
    poll = await crud.get_poll(session=session, poll_id=poll_id)
    if poll is not None:
        return poll

    raise exceptions.APIException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Poll {poll_id} not found!",
    )