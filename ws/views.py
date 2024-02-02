from typing import Annotated

import jwt
from fastapi import APIRouter, WebSocketDisconnect, WebSocket, Cookie, Query, WebSocketException, status, Depends

from api.auth.utils import decode_jwt
from api.users import crud
from core import exceptions
from core.models import User, Game, GameStatusEnum
from core.models.dependencies import DbSession
from ws.managers import manager

router = APIRouter(prefix="/ws", tags=["WS"])


async def get_payload(
    websocket: WebSocket,
    token: Annotated[str | None, Query()] = None,
):
    # websocket.scope['user'] = "SSS"
    # print(websocket.user)

    print(websocket.query_params.get("token"))

    try:
        jwt_payload = decode_jwt(token=token)
        return jwt_payload
    except jwt.exceptions.DecodeError:
        raise WebSocketException(code=22, reason="Invalid token")
    except jwt.exceptions.ExpiredSignatureError:
        raise WebSocketException(code=224, reason="Invalid token")


async def get_auth_user(
        session: DbSession,
        payload: Annotated[dict, Depends(get_payload)]

) -> User:
    user_id = payload.get("sub")
    auth_user: User = await crud.get_user(session=session, user_id=user_id)
    if not auth_user:
        raise WebSocketException(code=445, detail="Invalid token")
    return auth_user


@router.websocket("/{room_id}/{user_id}")
async def websocket_endpoint(
        websocket: WebSocket,
        room_id: int,
        user_id: int,
        current_user: Annotated[str, Depends(get_auth_user)]
):
    play_game = [game for game in current_user.room.games if game.status == GameStatusEnum.playing]

    if not len(play_game):
        raise WebSocketException()

    manager.group_add(group_name=f"room_{play_game[0].id}", websocket=websocket)
    manager.group_add(group_name=f"user_{current_user.id}", websocket=websocket)

    print(manager.active_connections)

    await manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            await websocket.send_text(f"Message text was: {data}")
            await manager.send_personal_message("", websocket)
    except WebSocketDisconnect:
        group = manager.get_group_by_client(websocket=websocket)
        manager.disconnect(websocket)
        await manager.broadcast(f"Client #{user_id} left the chat", group)
