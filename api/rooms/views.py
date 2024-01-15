from fastapi import APIRouter, HTTPException, status, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from core.models import db_helper
from . import crud
from .dependencies import get_room_by_id
from .schemas import Room, RoomCreate, RoomUpdate, RoomUpdatePartial

router = APIRouter(prefix="/rooms", tags=["Rooms"])


@router.get("/", response_model=list[Room])
async def get_rooms(
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
):
    return await crud.get_rooms(session=session)


@router.post("/", response_model=Room, status_code=status.HTTP_201_CREATED)
async def create_room(
    room_in: RoomCreate,
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
):
    return await crud.create_room(session=session, room_in=room_in)


@router.get("/join/{user_id}/",  response_model=Room, status_code=status.HTTP_201_CREATED)
async def join_in_room(
    user_id: int,
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
):
    return await crud.get_room_by_user(session=session, user_id=user_id)


@router.get("/{room_id}/", response_model=Room)
async def get_room(
    product: Room = Depends(get_room_by_id),
):
    return product


@router.put("/{room_id}/")
async def update_room(
    room_update: RoomUpdate,
    room: Room = Depends(get_room_by_id),
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
):
    return await crud.update_room(
        session=session,
        room=room,
        room_update=room_update,
    )


@router.patch("/{room_id}/")
async def update_room_partial(
    room_update: RoomUpdatePartial,
    room: Room = Depends(get_room_by_id),
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
):
    return await crud.update_room(
        session=session,
        room=room,
        room_update=room_update,
        partial=True,
    )


@router.delete("/{room_id}/", status_code=status.HTTP_204_NO_CONTENT)
async def delete_room(
    room: Room = Depends(get_room_by_id),
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
) -> None:
    await crud.delete_room(session=session, room=room)