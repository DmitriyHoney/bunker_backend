from typing import Annotated, Any

from fastapi import Path, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from auth.dependencies import CurrentUser
from core.models import db_helper, Game

from . import crud


async def get_game_by_id(
        game_id: Annotated[int, Path],
        session: AsyncSession = Depends(db_helper.scoped_session_dependency),
) -> Game:
    game = await crud.get_game(session=session, game_id=game_id)
    if game is not None:
        return game

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Product {game_id} not found!",
    )


class AuthFilter:
    def __init__(self, user=CurrentUser):
        self.user = user

    def filter_queryset(self, queryset: Any):
        if not self.user:
            return queryset


auth_filter = AuthFilter()
