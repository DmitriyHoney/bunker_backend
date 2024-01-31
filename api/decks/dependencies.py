from typing import Annotated

from fastapi import Path, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from api.auth.dependencies import Auth
from core.filters.base_filter import FilterDepends, with_prefix
from core.models import db_helper, Room

from . import crud
from .filters import DeckFilter

DeckFilterDepends = Annotated[DeckFilter, FilterDepends(DeckFilter)]


async def get_deck_by_id(
    deck_id: Annotated[int, Path],
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
) -> Room:
    deck = await crud.get_deck(session=session, deck_id=deck_id)
    if deck is not None:
        return deck

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Product {deck_id} not found!",
    )


async def get_deck_by_room_id(
        game_id: Annotated[int, Path],
        auth: Auth,
        session: AsyncSession = Depends(db_helper.scoped_session_dependency),
) -> Room:

    deck = await crud.get_deck_by_game_user(session=session, game_id=game_id, user_id=auth.id)
    if deck is not None:
        return deck

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f" {deck_id} not found!",
    )
