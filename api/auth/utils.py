import uuid
from datetime import datetime, timedelta
from typing import Annotated

import jwt
from fastapi import Depends, Request
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from core import exceptions
from core.config import settings
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from core.models import User, db_helper
from api.users import crud as user_crud


class UserAuth(BaseModel):
    uid: uuid.UUID
    id: int
    is_active: bool
    is_owner: bool

    @property
    def is_authenticated(self):
        return True


class UserAnonimous(BaseModel):
    uid: None = None
    id: None = None
    is_active: bool = False
    is_owner: bool = False

    @property
    def is_authenticated(self):
        return False


class AuthData(BaseModel):
    user: User | None = None
    credentials: HTTPAuthorizationCredentials | None = None
    is_authenticated: bool = False
    payload: dict | None = None

    class Config:
        arbitrary_types_allowed = True


http_bearer = HTTPBearer()


def encode_jwt(
        payload: dict,
        key: str = settings.auth_jwt.private_key_path.read_text(),
        algorithm: str = settings.auth_jwt.algorithm,
        expire_minutes=settings.auth_jwt.access_token_expire_minutes
) -> str:
    now = datetime.utcnow()
    expire = now + timedelta(minutes=expire_minutes)
    return jwt.encode(payload={'exp': expire, 'iat': now, **payload}, key=key, algorithm=algorithm)


def decode_jwt(
        token: str | bytes,
        key: str = settings.auth_jwt.public_key_path.read_text(),
        algorithm: str = settings.auth_jwt.algorithm,

) -> str:
    return jwt.decode(jwt=token, key=key, algorithms=[algorithm, ])


def get_auth_payload(
        credentials: HTTPAuthorizationCredentials = Depends(http_bearer),
) -> AuthData:

    auth_data = AuthData()
    try:
        jwt_payload = decode_jwt(token=credentials.credentials)
        auth_data.credentials = credentials
        auth_data.payload = jwt_payload
    except jwt.exceptions.DecodeError:
        raise exceptions.APIException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
    except jwt.exceptions.ExpiredSignatureError:
        raise exceptions.APIException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
    return auth_data


async def get_auth_user(
        request: Request,
        session: AsyncSession = Depends(db_helper.scoped_session_dependency),
        auth_data: AuthData = Depends(get_auth_payload)

) -> AuthData:
    user_id = auth_data.payload and auth_data.payload.get("sub")

    auth_user: UserAnonimous = await user_crud.get_user(session=session, user_id=user_id)
    if not auth_user:
        raise exceptions.APIException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")

    #print("ddddddddddddd", auth_user.model_dump_json())

    request.scope["user"] = auth_user
    auth_data.user = auth_user

    return auth_user



