from typing import Annotated

from fastapi import Path, Depends, HTTPException, status, Query
from sqlalchemy.ext.asyncio import AsyncSession

from core.models import db_helper, Game

from . import crud
from .schemas import RoundsFilterModel


async def rounds_filters(
    game_id: int | None = None
):
    return {'game_id': game_id}


RoundsFilterParams = Annotated[dict, Depends(rounds_filters)]


async def get_game_by_id(
    game_id: Annotated[int, Path],
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
) -> Game:
    game = await crud.get_game(session=session, game_id=game_id)
    if game is not None:
        return game

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Product {game_id} not found!",
    )