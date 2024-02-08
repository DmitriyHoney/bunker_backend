"""
Create
Read
Update
Delete
"""
import datetime

from sqlalchemy import select
from sqlalchemy.engine import Result
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from core import exceptions
from core.exceptions import APIException
from core.filters import Filter
from core.models import Game, Round, RoundStateEnum, Move, Poll
from .schemas import PollUpdate, PollUpdatePartial, PollCreate

Model = Poll


async def get_polls(session: AsyncSession, filters: Filter) -> list[Model]:
    query = select(Model).order_by(Model.id)
    query = filters.filter(query)
    if hasattr(filters, 'order_by'):
        query = filters.sort(query)
    result: Result = await session.execute(query)
    return result.scalars().all()


async def get_poll(session: AsyncSession, poll_id: int) -> Model | None:
    query = select(Model).where(Model.id == poll_id)
    result = await session.scalar(query)
    if not result:
        raise exceptions.APIException(status_code=status.HTTP_404_NOT_FOUND)
    return result


async def create_poll(session: AsyncSession, poll_in: PollCreate) -> Model:

    poll = Model(**poll_in.model_dump())
    session.add(poll)

    # await session.flush()
    # await session.refresh(game)
    #
    # users = game.room.users
    # random_decks = await get_random_cards_deck(session=session, limit=len(users))
    #
    # for i, user in enumerate(game.room.users):
    #     deck = Deck()
    #     deck.game = game
    #     deck.user = user
    #     deck.cards = random_decks[i]
    #     session.add(deck)
    #
    # create_rounds(game)
    #
    # for i in range(9):
    #     round = Round(name=f"round_{i + 1}")

    await session.commit()
    await session.refresh(poll)
    return poll


async def update_poll(
    session: AsyncSession,
    poll: Model,
    poll_update: PollUpdate | PollUpdatePartial,
    partial: bool = False,
) -> Model:
    for name, value in poll_update.model_dump(exclude_unset=partial).items():
        setattr(poll, name, value)
    await session.commit()
    return poll


async def delete_poll(
    session: AsyncSession,
    poll: Model,
) -> None:
    await session.delete(poll)
    await session.commit()


