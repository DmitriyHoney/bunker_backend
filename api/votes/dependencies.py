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


async def get_vote_by_id(
    vote_id: Annotated[int, Path],
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
) -> Game:
    vote = await crud.get_vote(session=session, vote_id=vote_id)
    if vote is not None:
        return vote

    raise exceptions.APIException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Vote {vote_id} not found!",
    )