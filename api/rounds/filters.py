from typing import Optional, Annotated, List

from fastapi.params import Query
from pydantic import Field

from core.filters import Filter
from core.filters.base_filter import FilterDepends
from core.models import Deck, Game, GameStatusEnum, Move, Round, RoundStateEnum


class RoundFilter(Filter):
    name: Annotated[Optional[str], Query(alias="name")] = None
    game_id: Annotated[Optional[int], Query(alias="game_id")] = None
    number: Annotated[Optional[int], Query(alias="number")] = None
    state: Annotated[Optional[RoundStateEnum], Query(alias="state")] = None
    search: Optional[str] = None

    class Constants(Filter.Constants):
        model = Round
        search_model_fields = ["name"]

    class Config:
        populate_by_name = True


RoundFilterDepends = Annotated[RoundFilter, FilterDepends(RoundFilter)]
