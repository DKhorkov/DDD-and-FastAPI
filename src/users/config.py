from dataclasses import dataclass
from typing import Tuple, Literal
from pydantic_settings import BaseSettings

from src.config import RouterConfig as BaseRouterConfig


@dataclass(frozen=True)
class URLPathsConfig:
    REGISTER: str = '/register'
    LOGIN: str = '/login'
    LOGOUT: str = '/logout'
    ME: str = '/me'
    VERIFY_EMAIL: str = '/verify-email/{token}'
    ALL: str = ''
    MY_STATS: str = '/get-my-statistics'
    LIKE_USER: str = '/{user_id}/like'
    DISLIKE_USER: str = '/{user_id}/dislike'


@dataclass(frozen=True)
class URLNamesConfig:
    REGISTER: str = 'register'
    LOGIN: str = 'login'
    LOGOUT: str = 'logout'
    ME: str = 'get my account'
    VERIFY_EMAIL: str = 'verify email'
    ALL: str = 'get all users'
    MY_STATS: str = 'get my statistics'
    LIKE_USER: str = 'like user'
    DISLIKE_USER: str = 'dislike user'


@dataclass(frozen=True)
class UserValidationConfig:
    PASSWORD_MIN_LENGTH: int = 8
    PASSWORD_MAX_LENGTH: int = 30
    USERNAME_MIN_LENGTH: int = 5
    USERNAME_MAX_LENGTH: int = 60


@dataclass(frozen=True)
class RouterConfig(BaseRouterConfig):
    PREFIX: str = '/users'
    TAGS: Tuple[str] = ('Users', )


class CookiesConfig(BaseSettings):
    COOKIES_KEY: str
    COOKIES_LIFESPAN_DAYS: int
    SECURE_COOKIES: bool
    HTTP_ONLY: bool
    SAME_SITE: Literal['strict', 'lax', 'none']


class PasslibConfig(BaseSettings):
    PASSLIB_SCHEME: str
    PASSLIB_DEPRECATED: str


cookies_config: CookiesConfig = CookiesConfig()
passlib_config: PasslibConfig = PasslibConfig()
