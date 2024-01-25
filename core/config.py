from pathlib import Path
from pydantic import BaseModel
from pydantic_settings import BaseSettings

BASE_DIR = Path(__file__).parent.parent

print(BASE_DIR)


class DbSettings(BaseModel):
    url: str = "postgresql+asyncpg://postgres:123@localhost/bunker"
    echo: bool = False


class AuthJWT(BaseModel):
    private_key_path: Path = BASE_DIR / "certs" / "jwt-private.pem"
    public_key_path: Path = BASE_DIR / "certs" / "jwt-public.pem"
    algorithm: str = "RS256"
    access_token_expire_minutes: int = 999999
    # access_token_expire_minutes: int = 3


class GameSettings(BaseModel):
    gamers_max_count: int = 16
    gamers_min_count: int = 6
    rounds_count: int = 8


class Settings(BaseSettings):
    api_prefix: str = "/api/v1"

    db: DbSettings = DbSettings()
    auth_jwt: AuthJWT = AuthJWT()
    game: GameSettings = GameSettings()
    # db_echo: bool = True


settings = Settings()
