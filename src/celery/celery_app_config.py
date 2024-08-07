from dataclasses import dataclass, field
from typing import Dict, Any, List, Tuple

from src.core.redis.connection import REDIS_URL
from src.celery.config import celery_config


@dataclass(frozen=True)
class CeleryAppConfig:
    broker_url: str
    result_backend: str
    include: List[str]

    beat_schedule: Dict[str, Any] = field(default_factory=dict)

    timezone: str = 'UTC'
    enable_utc: bool = True

    task_serializer: str = 'json'
    accept_content: Tuple[str] = ('json',)
    result_serializer: str = 'json'


DEFAULT_BROKER_URL: str = 'memory://localhost/'
DEFAULT_RESULT_BACKEND: str = 'rpc'

celery_app_config: CeleryAppConfig = CeleryAppConfig(
    broker_url=REDIS_URL if celery_config.USE_BROKER else DEFAULT_BROKER_URL,
    result_backend=REDIS_URL if celery_config.USE_RESULT_BACKEND else DEFAULT_RESULT_BACKEND,
    include=['src.celery.tasks.users_tasks']
)
