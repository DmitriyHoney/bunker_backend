from typing import Optional, Annotated, List

from fastapi.params import Query
from pydantic import Field

from core.filters import Filter
from core.models import Deck, Game


class DeckFilter(Filter):
    game_id: Annotated[Optional[int], Query(alias="game_id")] = None
    user_id: Annotated[Optional[int], Query(alias="user_id")] = None

    #search: Optional[int | str] = None
    #order_by: Optional[list[str]] = None

    class Constants(Filter.Constants):
        model = Deck
        #search_model_fields = ["game_id"]

    class Config:
        populate_by_name = True
