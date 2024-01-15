from fastapi import APIRouter
from starlette.websockets import WebSocketDisconnect, WebSocket

from ws.managers import manager

router = APIRouter(prefix="/ws", tags=["WS"])


@router.websocket("{room_id}/{user_id}")
async def websocket_endpoint(websocket: WebSocket, room_id: int, user_id: int):
    manager.group_add(group_name=f"room_{room_id}", websocket=websocket)
    manager.group_add(group_name=f"user_{user_id}", websocket=websocket)
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
        await manager.broadcast(f"Client #{client_id} left the chat", group)
