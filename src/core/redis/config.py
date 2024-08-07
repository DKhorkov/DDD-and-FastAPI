from pydantic_settings import BaseSettings


class RedisConfig(BaseSettings):
    REDIS_PASSWORD: str
    REDIS_HOST: str
    REDIS_PORT: int


redis_config: RedisConfig = RedisConfig()
