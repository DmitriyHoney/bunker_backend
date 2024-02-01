from typing import Annotated

from fastapi import Depends

from ws import manager
from ws.managers import ConnectionManager


def get_ws_manager() -> ConnectionManager:
    return manager


wsManager = Annotated[ConnectionManager, Depends(get_ws_manager)]
