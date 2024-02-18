from typing import Annotated

from fastapi import Path, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from core.models import db_helper, Round
from core.models.dependencies import DbSession

from . import crud


async def rounds_filters(
    game_id: int | None = None
):
    return {'game_id': game_id}


RoundsFilterParams = Annotated[dict, Depends(rounds_filters)]


async def get_round_by_id(
    round_id: Annotated[int, Path],
    session: DbSession,
) -> Round:
    round = await crud.get_round(session=session, round_id=round_id)
    if round is not None:
        return round

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Round {round_id} not found!",
    )