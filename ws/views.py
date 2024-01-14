from fastapi import APIRouter
from starlette.websockets import WebSocketDisconnect, WebSocket

from ws.managers import manager

router = APIRouter(prefix="/ws", tags=["WS"])


@router.websocket("/{client_id}")
async def websocket_endpoint(websocket: WebSocket, client_id: int):
    print(client_id)
    manager.group_add(group_name="common", websocket=websocket)
    await manager.connect(websocket)
    try:
        print(manager.active_connections)
        while True:
            data = await websocket.receive_text()
            await websocket.send_text(f"Message text was: {data}")
            await manager.send_personal_message("sdfsdfd", websocket)
    except WebSocketDisconnect:
        group = manager.get_group_by_client(websocket=websocket)
        manager.disconnect(websocket)
        await manager.broadcast(f"Client #{client_id} left the chat", group)
