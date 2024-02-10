from typing import Annotated, List, Any, Optional

from fastapi import APIRouter, HTTPException, status, Depends
from fastapi.params import Query
from sqlalchemy.ext.asyncio import AsyncSession

from core.filters import Filter
from core.filters.base_filter import with_prefix, FilterDepends
from core.models import db_helper
from core.models.dependencies import DbSession
from . import crud
from .dependencies import get_deck_by_id, get_deck_by_room_id, DeckFilterDepends
from .filters import DeckFilter
from .schemas import Deck, DeckCreate, DeckUpdate, DeckUpdatePartial

router = APIRouter(prefix="/api/v1/decks", tags=["Decks"])


@router.get("/", response_model=list[Deck])
async def get_decks(


    session: DbSession,
        filters: Optional[Filter] = FilterDepends(with_prefix("number_filter", DeckFilter)),

    lld: Annotated[List[Any], Query] = None,
):

    # sss = await filters.get_products_filter(session=session)
    # print(sss)

    return await crud.get_decks(session=session, filters=filters)


@router.post("/", response_model=Deck, status_code=status.HTTP_201_CREATED)
async def create_deck(
    deck_in: DeckCreate,
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
):
    return await crud.create_deck(session=session, deck_in=deck_in)


@router.post("/distribute/", response_model=list[Deck], status_code=status.HTTP_201_CREATED)
async def distribute_deck(
    deck_in: DeckCreate,
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
):
    return await crud.create_decks(session=session, deck_in=deck_in)


@router.get("/{deck_id}/", response_model=Deck)
async def get_deck(
    deck: Deck = Depends(get_deck_by_id),
):
    return deck


@router.get("/me", response_model=Deck)
async def get_user_deck(
    deck: Deck = Depends(get_deck_by_room_id),
):
    return deck


@router.put("/{deck_id}/")
async def update_deck(
    deck_update: DeckUpdate,
    deck: Deck = Depends(get_deck_by_id),
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
):
    return await crud.update_deck(
        session=session,
        deck=deck,
        deck_update=deck_update,
    )


@router.patch("/{deck_id}/")
async def update_deck_partial(
    deck_update: DeckUpdatePartial,
    deck: Deck = Depends(get_deck_by_id),
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
):
    return await crud.update_deck(
        session=session,
        deck=deck,
        deck_update=deck_update,
        partial=True,
    )


@router.delete("/{deck_id}/", status_code=status.HTTP_204_NO_CONTENT)
async def delete_deck(
    deck: Deck = Depends(get_deck_by_id),
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
) -> None:
    await crud.delete_deck(session=session, deck=deck)
