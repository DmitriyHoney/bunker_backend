from datetime import datetime, timedelta
import jwt
from fastapi import Depends, Request
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from core import exceptions
from core.config import settings
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials, OAuth2PasswordBearer

from core.models import User, db_helper
from api.users import crud as user_crud
from api.rooms import crud as room_crud

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


# oauth2_scheme = OAuth2PasswordBearer(tokenUrl='/auth/token/')


def get_auth_payload(
        credentials: HTTPAuthorizationCredentials = Depends(http_bearer),
):
    try:
        jwt_payload = decode_jwt(token=credentials.credentials)
        return jwt_payload
    except jwt.exceptions.DecodeError:
        raise exceptions.APIException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
    except jwt.exceptions.ExpiredSignatureError:
        raise exceptions.APIException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")


async def get_auth_user(
        request: Request,
        session: AsyncSession = Depends(db_helper.scoped_session_dependency),
        payload: dict = Depends(get_auth_payload)

) -> User:

    user_id = payload.get("sub")
    room_id = payload.get("room")
    auth_user = await user_crud.get_user(session=session, user_id=user_id)
    auth_room = await room_crud.get_room(session=session, room_id=room_id)
    if not auth_user:
        raise exceptions.APIException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")

    request.scope["user"] = auth_user

    return auth_user
