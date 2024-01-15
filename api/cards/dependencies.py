from typing import Annotated

from fastapi import Path, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from core.models import db_helper, Card

from . import crud


async def card_by_id(
    card_id: Annotated[int, Path],
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
) -> Card:
    card = await crud.get_card(session=session, card_id=card_id)
    if card is not None:
        return card

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Card {card_id} not found!",
    )

