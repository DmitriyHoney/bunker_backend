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
from core.models import Game, Round, RoundStateEnum, Move, Vote
from .schemas import VoteUpdate, VoteUpdatePartial, VoteCreate

Model = Vote


async def get_votes(session: AsyncSession, filters: Filter) -> list[Model]:
    query = select(Model).order_by(Model.id)
    query = filters.filter(query)
    if hasattr(filters, 'order_by'):
        query = filters.sort(query)
    result: Result = await session.execute(query)
    return result.scalars().all()


async def get_vote(session: AsyncSession, vote_id: int) -> Model | None:
    query = select(Model).where(Model.id == vote_id)
    result = await session.scalar(query)
    if not result:
        raise exceptions.APIException(status_code=status.HTTP_404_NOT_FOUND)
    return result


async def create_vote(session: AsyncSession, vote_in: VoteCreate) -> Model:

    vote = Model(**vote_in.model_dump())
    session.add(vote)

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
    await session.refresh(vote)
    return vote


async def update_vote(
    session: AsyncSession,
    vote: Model,
    vote_update: VoteUpdate | VoteUpdatePartial,
    partial: bool = False,
) -> Model:
    for name, value in vote_update.model_dump(exclude_unset=partial).items():
        setattr(vote, name, value)
    await session.commit()
    return vote


async def delete_vote(
    session: AsyncSession,
    vote: Model,
) -> None:
    await session.delete(vote)
    await session.commit()


