from typing import Optional, Annotated, List

from fastapi.params import Query
from pydantic import Field

from core.filters import Filter
from core.filters.base_filter import FilterDepends
from core.models import Deck, Game, GameStatusEnum, Move


class MoveFilter(Filter):
    round_id: Annotated[Optional[int], Query(alias="round_id")] = None
    user_id: Annotated[Optional[int], Query(alias="user_id")] = None
    card_id: Annotated[Optional[int], Query(alias="card_id")] = None

    #search: Optional[str] = None

    class Constants(Filter.Constants):
        model = Move
        search_model_fields = ["name"]

    class Config:
        populate_by_name = True


MoveFilterDepends = Annotated[MoveFilter, FilterDepends(MoveFilter)]
