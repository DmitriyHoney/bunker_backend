from typing import Annotated

from fastapi import Depends, Body
from starlette import status

from api.auth.utils import get_auth_user, AuthData
from api.users import crud as user_crud
from core.exceptions import APIException
from core.models import User
from core.models.dependencies import DbSession

CurrentUser = Annotated[User | None, Depends(get_auth_user)]

Auth = Annotated[AuthData, Depends(get_auth_user)]


async def get_user_by_id(
        user_id: Annotated[int, Body],
        session: DbSession,
) -> User:
    user = await user_crud.get_user(session=session, user_id=user_id)

    if user is None:
        raise APIException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User {user_id} not found!",
        )
    if not user.is_owner:
        raise APIException(
            detail="Пользователь должен быть создателем комнаты",
        )
    return user


async def get_game_by_room_id(
        room_id: Annotated[int, Body],
        session: DbSession,
) -> User:
    user = await user_crud.get_user(session=session, room_id=room_id)

    if user is None:
        raise APIException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Room {room_id} not found!",
        )
    if not user.is_owner:
        raise APIException(
            detail="Пользователь должен быть создателем комнаты",
        )
    return user
