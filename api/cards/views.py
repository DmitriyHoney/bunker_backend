from fastapi import APIRouter, status, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from core.models import db_helper
from ws import manager
from . import crud
from .dependencies import product_by_id
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
async def create_product(
    product_in: CardCreate,
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
):
    return await crud.create_product(session=session, product_in=product_in)


@router.get("/{product_id}/", response_model=Card)
async def get_product(
    product: Card = Depends(product_by_id),
):
    return product


@router.put("/{product_id}/")
async def update_product(
    product_update: CardUpdate,
    product: Card = Depends(product_by_id),
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
):
    return await crud.update_product(
        session=session,
        product=product,
        product_update=product_update,
    )


@router.patch("/{product_id}/")
async def update_product_partial(
    product_update: CardUpdatePartial,
    product: Card = Depends(product_by_id),
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
):
    return await crud.update_product(
        session=session,
        product=product,
        product_update=product_update,
        partial=True,
    )


@router.delete("/{product_id}/", status_code=status.HTTP_204_NO_CONTENT)
async def delete_product(
    product: Card = Depends(product_by_id),
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
) -> None:
    await crud.delete_product(session=session, product=product)
