from fastapi import APIRouter, status, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from core.models import db_helper
from ws import manager
from . import crud
from .dependencies import card_by_id
from .schemas import Card, CardCreate, CardUpdate, CardUpdatePartial

router = APIRouter(prefix="/cards", tags=["Cards"])


@router.get("/", response_model=list[Card])
async def get_cards(
    session: AsyncSession = Depends(db_helper.scoped_session_dependency)
):
    print("dddddddddddddd", manager.active_connections)

    for con in manager.active_connections:
        for mem in con.members:
            await manager.send_personal_message("Ghbdtn", mem)
        #return await crud.get_cards(session=session)
    return []


@router.post(
    "/",
    response_model=Card,
    status_code=status.HTTP_201_CREATED,
)
async def create_card(
    card_in: CardCreate,
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
):
    return await crud.create_card(session=session, card_in_in=card_in)


@router.get("/{card_id}/", response_model=Card)
async def get_card(
    card: Card = Depends(card_by_id),
):
    return card


@router.put("/{card_id}/")
async def update_product(
    card_update: CardUpdate,
    card: Card = Depends(card_by_id),
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
):
    return await crud.update_card(
        session=session,
        card=card,
        card_update=card_update,
    )


@router.patch("/{card_id}/")
async def update_card_partial(
    card_update: CardUpdatePartial,
    card: Card = Depends(card_by_id),
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
):
    return await crud.update_card(
        session=session,
        card=card,
        card_update=card_update,
        partial=True,
    )


@router.delete("/{card_id}/", status_code=status.HTTP_204_NO_CONTENT)
async def delete_card(
    card: Card = Depends(card_by_id),
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
) -> None:
    await crud.delete_card(session=session, card=card)