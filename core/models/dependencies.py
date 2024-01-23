from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from core.models import db_helper

DbSession = Annotated[AsyncSession,  Depends(db_helper.scoped_session_dependency)]

