from typing import Optional, Annotated, List

from fastapi.params import Query
from pydantic import Field

from core.filters import Filter
from core.filters.base_filter import FilterDepends
from core.models import Deck, Game, Card, CardCategoryEnum


class CardFilter(Filter):
    name: Annotated[Optional[str], Query(alias="name")] = None
    category: Annotated[Optional[CardCategoryEnum], Query(alias="category")] = None

    search: Optional[str] = None
    order_by: Optional[list[str]] = None

    class Constants(Filter.Constants):
        model = Card
        search_model_fields = ["name"]

    class Config:
        populate_by_name = True


CardFilterDepends = Annotated[CardFilter, FilterDepends(CardFilter)]
