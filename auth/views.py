from fastapi import APIRouter, HTTPException, status, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from core.models import db_helper
from .schemas import Token
from .utils import encode_jwt

router = APIRouter(prefix="/auth", tags=["Auth"])


@router.get("/token/", response_model=Token)
async def get_users(
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
):

    jwt_payload = {
        "sub": 1,
        "game": "1"
    }

    access = encode_jwt(payload=jwt_payload)
    token = Token(access=access)
    return token


