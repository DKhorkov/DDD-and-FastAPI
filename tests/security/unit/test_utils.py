import pytest
from datetime import datetime, timezone

from src.security.exceptions import InvalidTokenError
from src.security.models import JWTDataModel
from src.security.utils import parse_jwt_token, create_jwt_token


@pytest.mark.anyio
async def test_parse_jwt_token_fail_expired_token() -> None:
    jwt_data: JWTDataModel = JWTDataModel(user_id=1, exp=datetime.now(timezone.utc))
    token: str = await create_jwt_token(jwt_data=jwt_data)
    with pytest.raises(InvalidTokenError):
        await parse_jwt_token(token=token)


@pytest.mark.anyio
async def test_parse_jwt_token_fail_incorrect_token() -> None:
    with pytest.raises(InvalidTokenError):
        await parse_jwt_token(token='someIncorrectToken')


@pytest.mark.anyio
async def test_parse_jwt_token_success() -> None:
    jwt_data: JWTDataModel = JWTDataModel(user_id=1)
    token: str = await create_jwt_token(jwt_data=jwt_data)
    assert await parse_jwt_token(token=token)
