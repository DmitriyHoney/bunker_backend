from fastapi import APIRouter, HTTPException, status, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from core.models import db_helper
from . import crud
from .dependencies import get_user_by_id
from .schemas import Game, GameCreate, GameUpdate, GameUpdatePartial

router = APIRouter(prefix="/games", tags=["Games"])


@router.get("/", response_model=list[Game])
async def get_rooms(
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
):
    return await crud.get_games(session=session)


@router.post("/", response_model=Game, status_code=status.HTTP_201_CREATED)
async def create_games(
    user_in: GameCreate,
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
):
    return await crud.create_user(session=session, user_in=user_in)


@router.get("/{user_id}/", response_model=Game)
async def get_user(
    product: Game = Depends(get_user_by_id),
):
    return product


@router.put("/{user_id}/")
async def update_room(
    room_update: GameUpdate,
    room: Game = Depends(get_user_by_id),
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
):
    return await crud.update_room(
        session=session,
        room=room,
        room_update=room_update,
    )


@router.patch("/{user_id}/")
async def update_room_partial(
    room_update: GameUpdatePartial,
    room: Game = Depends(get_user_by_id),
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
):
    return await crud.update_room(
        session=session,
        room=room,
        room_update=room_update,
        partial=True,
    )


@router.delete("/{user_id}/", status_code=status.HTTP_204_NO_CONTENT)
async def delete_room(
    room: Game = Depends(get_user_by_id),
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
) -> None:
    await crud.delete_room(session=session, room=room)
