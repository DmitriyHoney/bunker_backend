from typing import Annotated

from fastapi import Depends

from auth.utils import get_auth_user, AuthData
from core.models import User

CurrentUser = Annotated[User | None, Depends(get_auth_user)]

Auth = Annotated[AuthData, Depends(get_auth_user)]


