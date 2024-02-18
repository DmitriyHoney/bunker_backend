import uuid
from datetime import datetime
from typing import Annotated
from uuid import UUID

from fastapi import Query
from pydantic import BaseModel, ConfigDict

from core.models import RoundStateEnum, GameStatusEnum
from core.models.poll import PollStatusEnum


class VotesFilterModel(BaseModel):
    pass


class VoteBase(BaseModel):
    pass
    #status: str


class VoteCreate(VoteBase):
    user_id: int
    poll_id: int
    exclude_user_id: int


class VoteUpdate(VoteCreate):
    pass


class VoteUpdatePartial(VoteCreate):
    pass


class VoteUser(BaseModel):
    id: int
    username: str

class VotePollRound(BaseModel):
    id: int


class VotePoll(BaseModel):
    id: int
    status: PollStatusEnum
    round: VotePollRound


class Vote(VoteBase):
    model_config = ConfigDict(from_attributes=True)
    id: int
    poll: VotePoll
    user: VoteUser
    exclude_user: VoteUser
