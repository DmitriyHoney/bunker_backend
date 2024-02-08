from fastapi import FastAPI, WebSocket
from fastapi.requests import Request
from fastapi.responses import JSONResponse
from fastapi import status
from fastapi.middleware import Middleware
from starlette.middleware.authentication import AuthenticationMiddleware

from api.cards.views import router as cards_router

from core.exceptions import APIException
from core.middlewares import BearerTokenAuthBackend
from middlewares import CustomHeaderMiddleware
from ws.views import router as ws_router

from api.auth.views import router as auth_router
from api.rooms.views import router as rooms_router
from api.users.views import router as users_router
from api.games.views import router as games_router
from api.decks.views import router as decks_router
from api.moves.views import router as moves_router
from api.rounds.views import router as rounds_router
from api.polls.views import router as polls_router


app = FastAPI(middleware=[Middleware(CustomHeaderMiddleware)])
app.include_router(auth_router)
app.include_router(rooms_router)
app.include_router(users_router)
app.include_router(games_router)
app.include_router(decks_router)
app.include_router(moves_router)
app.include_router(cards_router)
app.include_router(rounds_router)
app.include_router(polls_router)

app.include_router(ws_router)

#app.add_middleware(AuthenticationMiddleware, backend=BearerTokenAuthBackend())


@app.exception_handler(APIException)
def api_exceptions_handler(request: Request, exc: APIException):
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content={
            "status": "Error",
            "detail": exc.detail,
        })


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    while True:
        data = await websocket.receive_text()
        await websocket.send_text(f"Message text was: {data}")

