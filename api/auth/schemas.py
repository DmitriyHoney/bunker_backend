from pydantic import BaseModel, ConfigDict


class Token(BaseModel):
    access: str
    refresh: str
    token_type: str = "Bearer"


