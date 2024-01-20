from fastapi import APIRouter, HTTPException, status, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from core import exceptions
from core.models import db_helper, Card, Move
from . import crud
from .dependencies import get_move_by_id

from .schemas import MoveResponse, MovesCreate, MoveUpdate, MoveUpdatePartial
from ..cards.dependencies import get_card_by_id
from ..decks.crud import get_deck_by_game_user
from ..rooms.dependencies import get_room_by_id

router = APIRouter(prefix="/moves", tags=["Moves"])


@router.get("/", response_model=list[MoveResponse])
async def get_moves(
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
):
    return await crud.get_moves(session=session)


@router.get("/init", response_model=list[MoveResponse])
async def init_moves(
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
    move_in=MovesCreate
):
    return await crud.create_moves(session=session, move_in=move_in)


@router.post("/", response_model=MoveResponse, status_code=status.HTTP_201_CREATED)
async def create_moves(
    move_in: MovesCreate,
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
):
    return await crud.create_move(session=session, move_in=move_in)


@router.post("/make", response_model=MoveResponse, status_code=status.HTTP_201_CREATED)
async def make_move(
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
    move: Move = Depends(get_move_by_id),
    card: Card = Depends(get_card_by_id),
):

    if move.card:
        raise exceptions.APIException(detail="Ход уже сделан")

    deck = await get_deck_by_game_user(
        session=session,
        user_id=move.user.id,
        game_id=move.round and move.round.game.id
    )

    if card not in deck.cards:
        raise exceptions.APIException(detail="Карты нет в колоде игорока")
    deck.cards.remove(card)

    session.commit()

    return await crud.add_card_to_move(session=session, move=move, card=card)


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
