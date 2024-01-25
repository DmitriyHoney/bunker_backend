from fastapi import APIRouter, status, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from api.auth.dependencies import CurrentUser
from core.models import db_helper
from core.models.dependencies import DbSession
from . import crud
from .dependencies import get_game_by_id

from .schemas import Game, GameCreate, GameUpdate, GameUpdatePartial

router = APIRouter(prefix="/games", tags=["Games"])


@router.get("/", response_model=list[Game])
async def get_rooms(
        user: CurrentUser,
        session: DbSession,
):
    return await crud.get_games(session=session, user_id=user.id)


@router.post("/", response_model=Game, status_code=status.HTTP_201_CREATED)
async def create_games(
    game_in: GameCreate,
    session: DbSession,
):
    return await crud.create_game(session=session, game_in=game_in)


@router.get("/{game_id}/", response_model=Game)
async def get_game(
    game: Game = Depends(get_game_by_id),
):
    return game


@router.put("/{game_id}/")
async def update_game(
    session: DbSession,
    game_update: GameUpdate,
    game: Game = Depends(get_game_by_id),
):
    return await crud.update_game(
        session=session,
        game=game,
        game_update=game_update,
    )


@router.patch("/{game_id}/")
async def update_room_partial(
    game_update: GameUpdatePartial,
    game: Game = Depends(get_game_by_id),
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
):
    return await crud.update_room(
        session=session,
        game=game,
        game_update=game_update,
        partial=True,
    )


@router.delete("/{game_id}/", status_code=status.HTTP_204_NO_CONTENT)
async def delete_game(
    game: Game = Depends(get_game_by_id),
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
) -> None:
    await crud.delete_game(session=session, game=game)
