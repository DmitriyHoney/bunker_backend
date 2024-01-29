from typing import Optional

from fastapi_filter.contrib.sqlalchemy import Filter
from pydantic import Field
from sqlalchemy import select, Select
from sqlalchemy.ext.asyncio import AsyncSession

from core.models import Deck, Game


class DeckFilter(Filter):
    game_id: Optional[int] = Field(alias="games")

    class Constants(Filter.Constants):
        model = Deck

    class Config:
        populate_by_name = True
