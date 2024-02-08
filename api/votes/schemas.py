import uuid
from datetime import datetime
from typing import Annotated
from uuid import UUID

from fastapi import Query
from pydantic import BaseModel, ConfigDict

from core.models import RoundStateEnum, GameStatusEnum


class PollsFilterModel(BaseModel):
    pass


class PollBase(BaseModel):
    pass
    #status: str


class PollCreate(PollBase):
    round_id: int


class PollUpdate(PollCreate):
    pass


class PollUpdatePartial(PollCreate):
    pass


class PollVotesUser(BaseModel):
    id: int
    username: str


class PollVotes(BaseModel):
    id: int
    user: PollVotesUser
    exclude_user: PollVotesUser


class PollRound(BaseModel):
    name: str
    game_id: int
    state: RoundStateEnum
    number: int


class Poll(PollBase):
    model_config = ConfigDict(from_attributes=True)
    id: int
    round: PollRound
    votes: list[PollVotes]
