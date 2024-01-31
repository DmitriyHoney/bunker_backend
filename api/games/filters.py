from typing import Optional, Annotated, List

from fastapi.params import Query
from pydantic import Field

from core.filters import Filter
from core.filters.base_filter import FilterDepends
from core.models import Deck, Game, GameStatusEnum


class GameFilter(Filter):
    name: Annotated[Optional[str], Query(alias="name")] = None
    room_id: Annotated[Optional[int], Query(alias="room_id")] = None
    status: Annotated[Optional[GameStatusEnum], Query(alias="status")] = None

    search: Optional[str] = None

    class Constants(Filter.Constants):
        model = Game
        search_model_fields = ["name"]

    class Config:
        populate_by_name = True


GameFilterDepends = Annotated[GameFilter, FilterDepends(GameFilter)]
