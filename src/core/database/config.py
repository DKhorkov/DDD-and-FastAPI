from pydantic_settings import BaseSettings


class DatabaseConfig(BaseSettings):
    DATABASE_DIALECT: str
    DATABASE_DRIVER: str
    DATABASE_HOST: str
    DATABASE_PORT: int
    DATABASE_USER: str
    DATABASE_PASSWORD: str
    DATABASE_NAME: str
    DATABASE_ECHO: bool
    DATABASE_POOL_RECYCLE: int
    DATABASE_POOL_PRE_PING: bool
    DATABASE_AUTO_FLUSH: bool
    DATABASE_EXPIRE_ON_COMMIT: bool


database_config: DatabaseConfig = DatabaseConfig()
