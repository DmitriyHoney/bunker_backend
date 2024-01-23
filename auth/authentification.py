from typing import Optional

from fastapi import Depends, HTTPException
from fastapi import Request
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from fastapi.security.utils import get_authorization_scheme_param
from starlette.authentication import (
    AuthCredentials,
    AuthenticationBackend,
    AuthenticationError,
)
from starlette.requests import HTTPConnection
from starlette.responses import PlainTextResponse, Response
from starlette.status import HTTP_401_UNAUTHORIZED
from starlette.types import Scope

from auth.utils import get_auth_payload


class BasicAuthBackend(AuthenticationBackend):

    async def authenticate(self, conn, ):
        #print(conn.headers)
        if "authorization" not in conn.headers:
            return

        print(self.credentials.credentials)

        auth = conn.headers["authorization"]

        print(auth)

        try:
            scheme, credentials = auth.split()
            if scheme.lower() != 'basic':
                return
            decoded = base64.b64decode(credentials).decode("ascii")
        except (ValueError, UnicodeDecodeError, binascii.Error) as exc:
            raise AuthenticationError('Invalid basic auth credentials')

        username, _, password = decoded.partition(":")
        # TODO: You'd want to verify the username and password here.
        return AuthCredentials(["authenticated"]), SimpleUser(username)


class AuthenticationMiddleware:
    def __init__(self,
        payload: dict = Depends(get_auth_payload),
                 ) -> None:
        self.payload = payload

    async def __call__(self) -> None:
        scope = Scope
        print(self.scope["user"])

        # if scope["type"] not in ["http", "websocket"]:
        #     await self.app(scope, receive, send)
        #     return
        #
        # conn = HTTPConnection(scope)
        # try:
        #     auth_result = await self.backend.authenticate(conn)
        # except AuthenticationError as exc:
        #     response = self.on_error(conn, exc)
        #     if scope["type"] == "websocket":
        #         await send({"type": "websocket.close", "code": 1000})
        #     else:
        #         await response(scope, receive, send)
        #     return
        #
        # if auth_result is None:
        #     auth_result = AuthCredentials(), UnauthenticatedUser()
        # scope["auth"], scope["user"] = auth_result
        # await self.app(scope, receive, send)

    @staticmethod
    def default_on_error(conn: HTTPConnection, exc: Exception) -> Response:
        return PlainTextResponse(str(exc), status_code=400)


class OAuth2Bearer:
    def __init__(self):
        pass

    async def __call__(self, request: Request) -> Optional[str]:
        authorization = request.headers.get("Authorization")
        scheme, param = get_authorization_scheme_param(authorization)
        if not authorization or scheme.lower() != "bearer":
            if self.auto_error:
                raise HTTPException(
                    status_code=HTTP_401_UNAUTHORIZED,
                    detail="Not authenticated",
                    headers={"WWW-Authenticate": "Bearer"},
                )
            else:
                return None
        return param


    # def get_auth_payload(self,
    #         credentials: HTTPAuthorizationCredentials = Depends(http_bearer),
    # ):
    #     try:
    #         jwt_payload = decode_jwt(token=credentials.credentials)
    #         return jwt_payload
    #     except jwt.exceptions.DecodeError:
    #         raise exceptions.APIException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
    #     except jwt.exceptions.ExpiredSignatureError:
    #         raise exceptions.APIException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
    #
    # async def get_auth_user(
    #         session: AsyncSession = Depends(db_helper.scoped_session_dependency),
    #         payload: dict = Depends(get_auth_payload)
    # ) -> User:
    #
    #     user_id = payload.get("sub")
    #     auth_user = await user_crud.get_user(session=session, user_id=user_id)
    #     if not auth_user:
    #         raise exceptions.APIException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
    #     return auth_user


class BaseUser:
    @property
    def is_authenticated(self) -> bool:
        raise NotImplementedError()  # pragma: no cover

    @property
    def display_name(self) -> str:
        raise NotImplementedError()  # pragma: no cover

    @property
    def identity(self) -> int:
        raise NotImplementedError()  # pragma: no cover

    @property
    def game_identity(self) -> int:
        raise NotImplementedError()  # pragma: no cover


class SimpleUser(BaseUser):
    def __init__(self, user_id: int, game_id: int) -> None:
        self.game_id = game_id

    @property
    def is_authenticated(self) -> bool:
        return True

    @property
    def display_name(self) -> str:
        return self.username

    @property
    def identity(self) -> int:
        raise NotImplementedError()  # pragma: no cover

    @property
    def game_identity(self) -> int:
        raise NotImplementedError()  # pragma: no cover


class UnauthenticatedUser(BaseUser):

    @property
    def room(self) -> None:
        return None

    @property
    def is_authenticated(self) -> bool:
        return False

    @property
    def display_name(self) -> str:
        return ""