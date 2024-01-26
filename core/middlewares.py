import jwt
from starlette import status
from starlette.authentication import AuthenticationBackend, AuthenticationError,BaseUser

from api.auth.utils import decode_jwt
from api.users import crud
from core import exceptions
from core.models import db_helper


class BearerTokenAuthBackend(AuthenticationBackend):
    """
    This is a custom auth backend class that will allow you to authenticate your request and return auth and user as
    a tuple
    """
    async def authenticate(self, request):
        # This function is inherited from the base class and called by some other class

        if "Authorization" not in request.headers:
            return None, None

        auth = request.headers["Authorization"]

        try:
            scheme, token = auth.split()
            if scheme.lower() != 'bearer':
                return
            decoded = decode_jwt(token)

        except (ValueError, UnicodeDecodeError) as exc:
            raise exceptions.APIException("Invalid token")

        user_id: int = decoded.get("sub")

        async with db_helper.session_factory() as session:
            user = await crud.get_user(session=session, user_id=user_id)

        if user is None:
            raise exceptions.APIException("Invalid token")
        return auth, user