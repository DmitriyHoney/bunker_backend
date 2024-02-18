from typing import Optional, Annotated

from fastapi.params import Query

from core.filters import Filter
from core.filters.base_filter import FilterDepends
from core.models import Round, Vote


class VoteFilter(Filter):
    user_id: Annotated[Optional[int], Query(alias="user_id")] = None
    exclude_user_id: Annotated[Optional[int], Query(alias="exclude_user_id")] = None
    poll_id: Annotated[Optional[int], Query(alias="poll_id")] = None

    class Constants(Filter.Constants):
        model = Vote

    class Config:
        populate_by_name = True


VoteFilterDepends = Annotated[VoteFilter, FilterDepends(VoteFilter)]
