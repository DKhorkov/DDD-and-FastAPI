from pydantic_settings import BaseSettings


class JWTConfig(BaseSettings):
    JWT_TOKEN_SECRET_KEY: str
    JWT_TOKEN_ALGORITHM: str
    JWT_TOKEN_EXPIRE_DAYS: int


jwt_config: JWTConfig = JWTConfig()
