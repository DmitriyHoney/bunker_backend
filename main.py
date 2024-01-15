from typing import Union

from fastapi import FastAPI, WebSocket

from api.cards.views import router as cards_router
from ws.views import router as ws_router

from api.rooms.views import router as rooms_router
from api.users.views import router as users_router
from api.games.views import router as games_router

app = FastAPI()
app.include_router(rooms_router)
app.include_router(users_router)
app.include_router(games_router)

app.include_router(cards_router)
app.include_router(ws_router)

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    while True:
        data = await websocket.receive_text()
        await websocket.send_text(f"Message text was: {data}")


@app.get("/api/")
def read_root():
    return {"Hello": "World"}


@app.get("/api/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}
