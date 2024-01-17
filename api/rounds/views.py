from fastapi import APIRouter, HTTPException, status, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from core.models import db_helper
from . import crud
from .dependencies import get_game_by_id

from .schemas import Round, RoundCreate, RoundUpdate, RoundUpdatePartial
from ..rooms.dependencies import get_room_by_id

router = APIRouter(prefix="/rounds", tags=["Rounds"])


@router.get("/", response_model=list[Round])
async def get_rounds(
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
):
    return await crud.get_rounds(session=session)


@router.post("/", response_model=list[Round], status_code=status.HTTP_201_CREATED)
async def create_rounds(
    round_in: RoundCreate,
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
):
    return await crud.create_rounds(session=session, round_in=round_in)


@router.put("/{game_id}/")
async def update_game(
    game_update: RoundUpdate,
    game: Round = Depends(get_game_by_id),
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
):
    return await crud.update_game(
        session=session,
        game=game,
        game_update=game_update,
    )


@router.patch("/{game_id}/")
async def update_room_partial(
    game_update: RoundUpdatePartial,
    game: Round = Depends(get_game_by_id),
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
):
    return await crud.update_room(
        session=session,
        game=game,
        game_update=game_update,
        partial=True,
    )


@router.delete("/{game_id}/", status_code=status.HTTP_204_NO_CONTENT)
async def delete_game(
    game: Round = Depends(get_game_by_id),
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
) -> None:
    await crud.delete_game(session=session, game=game)
