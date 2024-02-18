from typing import Annotated

from fastapi import APIRouter, HTTPException, status, Depends, Body
from sqlalchemy.ext.asyncio import AsyncSession

from core.models import db_helper, User
from .dependencies import get_user_by_id
from .schemas import Token
from .utils import encode_jwt


router = APIRouter(prefix="/api/v1/auth", tags=["Auth"])


@router.get("token/test/", response_model=Token)
async def get_test_token(
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
):

    jwt_payload = {
        "sub": 1,
        "game": "1"
    }

    access = encode_jwt(payload=jwt_payload)
    token = Token(access=access)
    return token


@router.post("/token/", response_model=Token)
async def get_token(
    user: Annotated[User, Depends(get_user_by_id)]
):
    print(user)
    jwt_payload = {
        "sub": user.id,
    }
    access = encode_jwt(payload=jwt_payload)
    token = Token(access=access)
    return token


