from fastapi import APIRouter, HTTPException, status, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from core.models import db_helper
from . import crud
from .dependencies import get_move_by_id

from .schemas import Move, MovesCreate, MoveUpdate, MoveUpdatePartial
from ..rooms.dependencies import get_room_by_id

router = APIRouter(prefix="/moves", tags=["Moves"])


@router.get("/", response_model=list[Move])
async def get_moves(
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
):
    return await crud.get_moves(session=session)


@router.post("/", response_model=Move, status_code=status.HTTP_201_CREATED)
async def create_moves(
    move_in: MovesCreate,
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
):
    return await crud.create_move(session=session, move_in=move_in)


@router.get("/{move_id}/", response_model=Move)
async def get_game(
    move: Move = Depends(get_move_by_id),
):
    return move


@router.put("/{move_id}/")
async def update_move(
    move_update: MoveUpdate,
    move: Move = Depends(get_move_by_id),
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
):
    return await crud.update_move(
        session=session,
        move=move,
        move_update=move_update,
    )


@router.patch("/{move_id}/")
async def update_room_partial(
    move_update: MoveUpdatePartial,
    move: Move = Depends(get_move_by_id),
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
):
    return await crud.update_room(
        session=session,
        move=move,
        move_update=move_update,
        partial=True,
    )


@router.delete("/{move_id}/", status_code=status.HTTP_204_NO_CONTENT)
async def delete_move(
    move: Move = Depends(get_move_by_id),
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
) -> None:
    await crud.delete_move(session=session, move=move)
