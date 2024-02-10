from fastapi import APIRouter, status, Depends, Request, BackgroundTasks
from sqlalchemy.ext.asyncio import AsyncSession

from core import exceptions
from core.models import db_helper, Card, Move
from core.models.dependencies import DbSession
from ws import manager
from ws.dependencies import wsManager
from . import crud
from .dependencies import get_move_by_id
from .filters import MoveFilterDepends

from .schemas import MoveResponse, MoveCreate, MoveUpdate, MoveUpdatePartial
from .sevices import remove_card_in_deck, make_move_card
from ..auth.dependencies import Auth
from ..cards.dependencies import get_card_by_id


router = APIRouter(prefix="/api/v1/moves", tags=["Moves"])


@router.get("/", response_model=list[MoveResponse])
async def get_moves(
        filters: MoveFilterDepends,
        ws_manager: wsManager,
        background_tasks: BackgroundTasks,
        session: AsyncSession = Depends(db_helper.scoped_session_dependency),
):

    background_tasks.add_task(ws_manager.broadcast, "ddddd", ws_manager.get_group_by_name('user_1'))
    return await crud.get_moves(session=session, filters=filters)


# @router.get("/init", response_model=list[MoveResponse])
# async def init_moves(
#     session: AsyncSession = Depends(db_helper.scoped_session_dependency),
#     move_in=MoveCreate
# ):
#     return await crud.create_moves(session=session, move_in=move_in)


@router.post("/", response_model=MoveResponse, status_code=status.HTTP_201_CREATED)
async def create_moves(
    move_in: MoveCreate,
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
):
    return await crud.create_move(session=session, move_in=move_in)


@router.post("/make", response_model=MoveResponse, status_code=status.HTTP_201_CREATED)
async def make_move(
    session: DbSession,
    auth: Auth,
    request: Request,
    ws_manager: wsManager,
    background_tasks: BackgroundTasks,
    move: Move = Depends(get_move_by_id),
    card: Card = Depends(get_card_by_id),

):
    #ws_manager.get_group_by_name()
    print(ws_manager.active_connections)
    print(card)

    ("ddddddddddddd", auth)
    if request.user and not move.user == request.user:
        exceptions.APIException(detail=f"Ход не может сделать игрок {request.user.id}")

    move = await make_move_card(session=session, move=move, card=card, user=request.user)
    background_tasks.add_task()
    return move


@router.get("/{move_id}/", response_model=MoveResponse)
async def get_game(
    move: Move = Depends(get_move_by_id),
):
    return move


@router.put("/{move_id}/")
async def update_move(
    move_update: MoveUpdate,
    move: Move = Depends(get_move_by_id),
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
):
    return await crud.update_move(
        session=session,
        move=move,
        move_update=move_update,
    )


@router.patch("/{move_id}/")
async def update_room_partial(
    move_update: MoveUpdatePartial,
    move: Move = Depends(get_move_by_id),
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
):
    return await crud.update_room(
        session=session,
        move=move,
        move_update=move_update,
        partial=True,
    )


@router.delete("/{move_id}/", status_code=status.HTTP_204_NO_CONTENT)
async def delete_move(
    move: Move = Depends(get_move_by_id),
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
) -> None:
    await crud.delete_move(session=session, move=move)
