from typing import Annotated

from fastapi import APIRouter, status, Depends, Body

from core.models import Round
from core.models.dependencies import DbSession
from . import crud
from .dependencies import get_poll_by_id
from .filters import PollFilterDepends
from .schemas import Poll, PollCreate, PollUpdate, PollUpdatePartial
from ..rounds.dependencies import get_round_by_id

router = APIRouter(prefix="/polls", tags=["Polls"])


@router.get("/", response_model=list[Poll])
async def get_polls(
    session: DbSession,
    filters: PollFilterDepends,
):
    return await crud.get_polls(session=session, filters=filters)


@router.post("/", response_model=Poll, status_code=status.HTTP_201_CREATED)
async def create_poll(
    session: DbSession,
    poll_create: Annotated[PollCreate, Body],
):
    return await crud.create_poll(session=session, poll_in=poll_create)


@router.put("/{poll_id}/")
async def update_poll(
    session: DbSession,
    poll_update: PollUpdate,
    poll: Poll = Depends(get_poll_by_id),

):
    return await crud.update_poll(
        session=session,
        poll=poll,
        poll_update=poll_update,
    )


@router.patch("/{poll_id}/")
async def update_room_partial(
    session: DbSession,
    game_update: PollUpdatePartial,
    poll: Poll = Depends(get_poll_by_id),

):
    return await crud.update_poll(
        session=session,
        poll=poll,
        poll_update=game_update,
        partial=True,
    )

@router.delete("/{poll_id}/", status_code=status.HTTP_204_NO_CONTENT)
async def delete_poll(
        session: DbSession,
        poll: Poll = Depends(get_poll_by_id),
) -> None:
    await crud.delete_poll(session=session, poll=poll)
