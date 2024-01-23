from pydantic import BaseModel, ConfigDict


class Token(BaseModel):
    access: str
    refresh: str | None = None
    token_type: str = "Bearer"


