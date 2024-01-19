from typing import Any, Optional, Dict

from fastapi import HTTPException
from fastapi import status


class ApiException(HTTPException):
    def __init__(
            self,
            status_code: int = status.HTTP_400_BAD_REQUEST,
            detail: Any = None,
            headers: Optional[Dict[str, str]] = None,
            ) -> None:
        super().__init__(status_code=status_code, detail=detail, headers=headers)
