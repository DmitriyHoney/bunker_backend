from typing import Annotated

from fastapi import APIRouter, status, Depends, Body
from sqlalchemy.ext.asyncio import AsyncSession

from core.models import db_helper
from . import crud
from .dependencies import get_round_by_id
from .filters import RoundFilterDepends
from .schemas import Round, RoundCreate, RoundUpdate, RoundUpdatePartial

router = APIRouter(prefix="/rounds", tags=["Rounds"])


@router.get("/", response_model=list[Round])
async def get_rounds(
    filters: RoundFilterDepends,
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),

):

    print(filters)

    return await crud.get_rounds(session=session, filters=filters)


@router.post("/", response_model=list[Round], status_code=status.HTTP_201_CREATED)
async def create_rounds(
    round_create: Annotated[RoundCreate, Body],
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
):
    return await crud.create_rounds(session=session, game_id=round_create.game_id)


@router.put("/{round_id}/")
async def update_round(
    game_update: RoundUpdate,
    game: Round = Depends(get_round_by_id),
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
):
    return await crud.update_game(
        session=session,
        game=game,
        game_update=game_update,
    )


@router.patch("/{round_id}/")
async def update_round_partial(
    game_update: RoundUpdatePartial,
    game: Round = Depends(get_round_by_id),
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
):
    return await crud.update_game(
        session=session,
        game=game,
        game_update=game_update,
        partial=True,
    )


@router.delete("/{round_id}/", status_code=status.HTTP_204_NO_CONTENT)
async def delete_round(
    game: Round = Depends(get_round_by_id),
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
) -> None:
    await crud.delete_game(session=session, game=game)
