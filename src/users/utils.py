from fastapi import Request
from fastapi.security import OAuth2
from fastapi.openapi.models import OAuthFlows as OAuthFlowsModel
from passlib.context import CryptContext
from typing import Optional, Dict

from src.users.config import URLPathsConfig, cookies_config, passlib_config, RouterConfig
from src.users.exceptions import NotAuthenticatedError


class OAuth2Cookie(OAuth2):
    """
    Class uses OAuth2 to retrieve token for user authentication from cookies.
    """

    def __init__(
        self,
        token_url: str,
        scheme_name: Optional[str] = None,
        scopes: Optional[Dict[str, str]] = None,
        description: Optional[str] = None,
        auto_error: bool = True,
    ):
        if not scopes:
            scopes = {}
        flows = OAuthFlowsModel(password={'tokenUrl': token_url, 'scopes': scopes})
        super().__init__(
            flows=flows,
            scheme_name=scheme_name,
            description=description,
            auto_error=auto_error,
        )

    async def __call__(self, request: Request) -> Optional[str]:
        """
        Retrieves token for user authentication from cookies, if exists.
        """

        token: Optional[str] = request.cookies.get(cookies_config.COOKIES_KEY)
        if not token:
            if self.auto_error:
                raise NotAuthenticatedError
            else:
                return None
        return token


pwd_context: CryptContext = CryptContext(
    schemes=[passlib_config.PASSLIB_SCHEME],
    deprecated=passlib_config.PASSLIB_DEPRECATED
)

oauth2_scheme: OAuth2Cookie = OAuth2Cookie(token_url=RouterConfig.PREFIX + URLPathsConfig.LOGIN)


async def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(secret=plain_password, hash=hashed_password)


async def hash_password(password: str) -> str:
    return pwd_context.hash(secret=password)
