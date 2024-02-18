from typing import Annotated

from fastapi import APIRouter, status, Depends, Body

from core.models.dependencies import DbSession
from . import crud
from .dependencies import get_vote_by_id
from .filters import VoteFilterDepends
from .schemas import Vote, VoteCreate, VoteUpdate, VoteUpdatePartial


router = APIRouter(prefix="/api/v1/votes", tags=["Votes"])


@router.get("/", response_model=list[Vote])
async def get_votes(
    session: DbSession,
    filters: VoteFilterDepends,
):
    return await crud.get_votes(session=session, filters=filters)


@router.post("/", response_model=Vote, status_code=status.HTTP_201_CREATED)
async def create_vote(
    session: DbSession,
    poll_create: Annotated[VoteCreate, Body],
):
    return await crud.create_poll(session=session, poll_in=poll_create)


@router.put("/{vote_id}/")
async def update_vote(
    session: DbSession,
    vote_update: VoteUpdate,
    vote: Vote = Depends(get_vote_by_id),

):
    return await crud.update_vote(
        session=session,
        vote=vote,
        vote_update=vote_update,
    )


@router.patch("/{vote_id}/")
async def update_vote_partial(
    session: DbSession,
    vote_update: VoteUpdatePartial,
    vote: Vote = Depends(get_vote_by_id),

):
    return await crud.update_vote(
        session=session,
        vote=vote,
        vote_update=vote_update,
        partial=True,
    )

@router.delete("/{vote_id}/", status_code=status.HTTP_204_NO_CONTENT)
async def delete_vote(
        session: DbSession,
        vote: Vote = Depends(get_vote_by_id),
) -> None:
    await crud.delete_vote(session=session, vote=vote)
