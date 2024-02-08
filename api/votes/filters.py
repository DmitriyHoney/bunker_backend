from typing import Optional, Annotated

from fastapi.params import Query

from core.filters import Filter
from core.filters.base_filter import FilterDepends
from core.models import Round


class PollFilter(Filter):
    round_id: Annotated[Optional[int], Query(alias="game_id")] = None

    class Constants(Filter.Constants):
        model = Round

    class Config:
        populate_by_name = True


PollFilterDepends = Annotated[PollFilter, FilterDepends(PollFilter)]
