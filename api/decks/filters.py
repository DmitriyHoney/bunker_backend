from typing import Optional, Annotated, List

from pydantic import Field

from core.filters import Filter
from core.models import Deck, Game


class DeckFilter(Filter):
    game_id: Annotated[Optional[int], Field(alias="game_id")] = None
    search: Optional[int | str] = None
    order_by: str = None

    class Constants(Filter.Constants):
        model = Deck
        search_model_fields = ["game_id"]

    class Config:
        populate_by_name = True
