"""
Create
Read
Update
Delete
"""
from random import random

from sqlalchemy import select, func
from sqlalchemy.engine import Result, ScalarResult
from sqlalchemy.ext.asyncio import AsyncSession
from core.models import Card, CardCategoryEnum
from core.models.card import card_user_categories

from .schemas import CardCreate, CardUpdate, CardUpdatePartial, CardSet


async def get_cards(session: AsyncSession) -> list[Card]:
    stmt = select(Card).order_by(Card.id)
    result: Result = await session.execute(stmt)
    products = result.scalars().all()
    return list(products)


async def get_card(session: AsyncSession, card_id: int) -> Card | None:
    return await session.get(Card, card_id)


async def get_random_cards(session: AsyncSession,
                           card_category: CardCategoryEnum,
                           limit: int,
                           ) -> Card | None:

    query = select(Card).where(Card.category == card_category).order_by(func.random()).limit(limit)
    #result: Result = await session.execute(query)
    result: ScalarResult = await session.scalars(query)
    return result.all()


async def get_random_cards_deck(session: AsyncSession, limit: int) -> list[list[Card]]:
    decks = [list() for _ in range(limit)]
    for category in card_user_categories:
        cards = await get_random_cards(session=session, card_category=category, limit=limit)
        for i, card in enumerate(cards):
            decks[i].append(card)
    return decks


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
