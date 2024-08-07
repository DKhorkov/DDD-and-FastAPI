from src.core.redis.config import redis_config


REDIS_URL: str = 'redis://:{}@{}:{}'.format(
    redis_config.REDIS_PASSWORD,
    redis_config.REDIS_HOST,
    redis_config.REDIS_PORT
)
