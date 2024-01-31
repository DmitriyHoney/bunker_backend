import uuid
from typing import Optional, Annotated, List

from fastapi.params import Query
from pydantic import Field

from core.filters import Filter
from core.filters.base_filter import FilterDepends
from core.models import Deck, Game, GameStatusEnum, Move, Round, RoundStateEnum, User


class UserFilter(Filter):
    username: Annotated[Optional[str], Query(alias="username")] = None
    room_id: Annotated[Optional[int], Query(alias="room_id")] = None
    is_owner: Annotated[Optional[bool], Query(alias="is_owner")] = None
    uid: Annotated[Optional[uuid.UUID], Query(alias="uid")] = None
    search: Optional[str] = None

    class Constants(Filter.Constants):
        model = User
        search_model_fields = ["username"]

    class Config:
        populate_by_name = True


UserFilterDepends = Annotated[UserFilter, FilterDepends(UserFilter)]
