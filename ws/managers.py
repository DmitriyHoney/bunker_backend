from pydantic import BaseModel
from starlette.websockets import WebSocket


class Group(BaseModel):
    name: str
    members: list[WebSocket] = []

    class Config:
        arbitrary_types_allowed = True


class ConnectionManager:
    def __init__(self):
        self.active_connections: list[Group] = []

    def get_group_by_name(self, group_name: str):
        group = next(
            (group for group in self.active_connections if group.name == group_name),
            None,
        )
        if group:
            return group
        return Group(name=group_name)

    def get_group_by_client(self, websocket: WebSocket):
        return next(
            (group for group in self.active_connections if websocket in group.members),
            None,
        )

    def group_add(self, group_name: str, websocket: WebSocket):
        group = self.get_group_by_name(group_name)
        group.members.append(websocket)
        if group not in self.active_connections:
            self.active_connections.append(group)

    async def connect(self, websocket: WebSocket):
        await websocket.accept()

    def disconnect(self, websocket: WebSocket):
        group = self.get_group_by_client(websocket)
        if group:
            group.members.remove(websocket)

    async def send_personal_message(self, message: str, websocket: WebSocket):
        await websocket.send_text(message)

    async def broadcast(self, message: str, group: Group):
        for connection in group.members:
            await connection.send_text(message)


    async def broadcast(self, message: str, group: Group):
        for connection in group.members:
            await connection.send_text(message)

manager = ConnectionManager()
