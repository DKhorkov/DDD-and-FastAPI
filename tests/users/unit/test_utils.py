import pytest
from starlette.requests import Request
from typing import Dict

from src.users.config import URLPathsConfig
from src.users.exceptions import NotAuthenticatedError
from src.users.utils import hash_password, verify_password, OAuth2Cookie
from tests.config import FakeUserConfig
from tests.utils import build_request


@pytest.mark.anyio
async def test_verify_password_success() -> None:
    hashed_password: str = await hash_password(FakeUserConfig.PASSWORD)
    assert await verify_password(plain_password=FakeUserConfig.PASSWORD, hashed_password=hashed_password)


@pytest.mark.anyio
async def test_verify_password_fail() -> None:
    hashed_password: str = await hash_password('some other password')
    assert not await verify_password(plain_password=FakeUserConfig.PASSWORD, hashed_password=hashed_password)


@pytest.mark.anyio
async def test_oauth2cookie_success() -> None:
    oauth2cookie: OAuth2Cookie = OAuth2Cookie(token_url=URLPathsConfig.LOGIN)
    headers: Dict[str, str] = {
        'cookie':
            'Access-Token=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoxLCJleHAiOjE3MTQ4NTgwOTd9.'
            'v4yKYGx0O5SxdL3hy37KM2f50W8TZNFeNDtk3zkTibs'
    }

    request: Request = build_request(headers=headers)
    assert await oauth2cookie(request)


@pytest.mark.anyio
async def test_oauth2cookie_fail_without_auto_error() -> None:
    oauth2cookie: OAuth2Cookie = OAuth2Cookie(token_url=URLPathsConfig.LOGIN, auto_error=False)
    request: Request = build_request()
    assert not await oauth2cookie(request)


@pytest.mark.anyio
async def test_oauth2cookie_fail_with_auto_error() -> None:
    with pytest.raises(NotAuthenticatedError):
        oauth2cookie: OAuth2Cookie = OAuth2Cookie(token_url=URLPathsConfig.LOGIN)
        request: Request = build_request()
        await oauth2cookie(request)
