from dataclasses import dataclass
from pydantic_settings import BaseSettings

from src.config import PathsConfig as BasePathsConfig


@dataclass(frozen=True)
class PathsConfig(BasePathsConfig):
    EMAIL_TEMPLATES: str = BasePathsConfig.TEMPLATES + 'email_templates/'
    VOTE_FOR_USER_EMAIL_TEMPLATE: str = 'vote_for_user_email.html'


@dataclass(frozen=True)
class EmailSubjectsConfig(BasePathsConfig):
    VOTED_FOR_USER: str = 'Оценка пользователя'


class SMTPConfig(BaseSettings):
    SMTP_HOST: str
    SMTP_PORT: int
    SMTP_LOGIN: str
    SMTP_PASSWORD: str


class CeleryConfig(BaseSettings):
    USE_BROKER: bool
    USE_RESULT_BACKEND: bool


smtp_config: SMTPConfig = SMTPConfig()
celery_config: CeleryConfig = CeleryConfig()
