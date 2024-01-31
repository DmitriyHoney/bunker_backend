import uuid
from typing import Optional, Annotated, List

from fastapi.params import Query
from pydantic import Field

from core.filters import Filter
from core.filters.base_filter import FilterDepends
from core.models import Deck, Game, GameStatusEnum, Move, Round, RoundStateEnum, Room


class RoomFilter(Filter):
    name: Annotated[Optional[str], Query(alias="name")] = None
    uid: Annotated[Optional[uuid.UUID], Query(alias="uid")] = None

    search: Optional[str] = None

    class Constants(Filter.Constants):
        model = Room
        search_model_fields = ["name"]

    class Config:
        populate_by_name = True


RoomFilterDepends = Annotated[RoomFilter, FilterDepends(RoomFilter)]
