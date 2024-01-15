from typing import Annotated

from fastapi import Path, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from core.models import db_helper, Room

from . import crud


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
