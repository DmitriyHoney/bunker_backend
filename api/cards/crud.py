"""
Create
Read
Update
Delete
"""

from sqlalchemy import select, func
from sqlalchemy.engine import Result
from sqlalchemy.ext.asyncio import AsyncSession
from core.models import Card, CardCategoryEnum

from .schemas import CardCreate, CardUpdate, CardUpdatePartial


async def get_cards(session: AsyncSession) -> list[Card]:
    stmt = select(Card).order_by(Card.id)
    result: Result = await session.execute(stmt)
    products = result.scalars().all()
    return list(products)


async def get_card(session: AsyncSession, card_id: int) -> Card | None:
    return await session.get(Card, card_id)


async def get_random_card(session: AsyncSession,
                          card_category: CardCategoryEnum,
                          black_list: list[int],
                          game_id: int,
                          ) -> Card | None:
    return await session.scalar(select(Card).where(Card.category == card_category,
                                                   Card.id.not_in(black_list)).order_by(func.random()))


async def create_card(session: AsyncSession, card_in: CardCreate) -> Card:
    card = Card(**card_in.model_dump())
    session.add(card)
    await session.commit()
    # await session.refresh(card)
    return card


async def update_card(
    session: AsyncSession,
    card: Card,
    card_update: CardUpdate | CardUpdatePartial,
    partial: bool = False,
) -> Card:
    for name, value in card_update.model_dump(exclude_unset=partial).items():
        setattr(card, name, value)
    await session.commit()
    return card


async def delete_card(
    session: AsyncSession,
    card: Card,
) -> None:
    await session.delete(card)
    await session.commit()
