from fastapi import APIRouter, status, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from core.models import db_helper
from . import crud
from .dependencies import get_user_by_id
from .schemas import User, UserCreate, UserUpdate, UserUpdatePartial, UserCreateResponse
from api.auth.schemas import Token
from api.auth.utils import encode_jwt

router = APIRouter(prefix="/users", tags=["Users"])


@router.get("/", response_model=list[User])
async def get_users(
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
):
    return await crud.get_users(session=session)


@router.post("/", response_model=UserCreateResponse, status_code=status.HTTP_201_CREATED)
async def create_user(
    user_in: UserCreate,
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
):
    user = await crud.create_user(session=session, user_in=user_in)
    access = encode_jwt(payload={
        "sub": user.id,
        "room": user_in.room_id
    })
    token = Token(access=access)
    user.token = token
    return user


@router.get("/{user_id}/", response_model=User)
async def get_user(
    product: User = Depends(get_user_by_id),
):
    return product


@router.put("/{user_id}/")
async def update_room(
    room_update: UserUpdate,
    room: User = Depends(get_user_by_id),
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
):
    return await crud.update_room(
        session=session,
        room=room,
        room_update=room_update,
    )


@router.patch("/{user_id}/")
async def update_room_partial(
    room_update: UserUpdatePartial,
    room: User = Depends(get_user_by_id),
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
    room: User = Depends(get_user_by_id),
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
) -> None:
    await crud.delete_room(session=session, room=room)
