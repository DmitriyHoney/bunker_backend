from typing import Annotated

from fastapi import APIRouter, WebSocketDisconnect, WebSocket, Cookie, Query, WebSocketException, status, Depends

from ws.managers import manager

router = APIRouter(prefix="/ws", tags=["WS"])


async def get_cookie_or_token(
    websocket: WebSocket,
    session: Annotated[str | None, Cookie()] = None,
    token: Annotated[str | None, Query()] = None,
):

    print(session)
    # if session is None and token is None:
    #     raise WebSocketException(code=status.WS_1008_POLICY_VIOLATION)
    return session or token



@router.websocket("/{room_id}/{user_id}")
async def websocket_endpoint(
        websocket: WebSocket,
        room_id: int,
        user_id: int,
        cookie_or_token: Annotated[str, Depends(get_cookie_or_token)]
):
    print(cookie_or_token)
    manager.group_add(group_name=f"room_{room_id}", websocket=websocket)
    manager.group_add(group_name=f"user_{user_id}", websocket=websocket)
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
