import pytest
from fastapi import status
from httpx import Response, AsyncClient, Cookies
from typing import Dict, Any

from src.users.config import RouterConfig, URLPathsConfig, cookies_config
from src.users.constants import ErrorDetails
from tests.utils import get_error_message_from_response


@pytest.mark.anyio
async def test_get_my_statistics_success(
        async_client: AsyncClient,
        create_test_user: None,
        cookies: Cookies
) -> None:

    response: Response = await async_client.get(
        url=RouterConfig.PREFIX + URLPathsConfig.MY_STATS,
        cookies=cookies
    )

    assert response.status_code == status.HTTP_200_OK

    response_content: Dict[str, Any] = response.json()
    assert response_content['likes'] == 0
    assert response_content['dislikes'] == 0


@pytest.mark.anyio
async def test_get_my_statistics_fail(async_client: AsyncClient, create_test_user: None) -> None:
    # Deleting cookies from async client, because if used as a "session" fixture:
    async_client.cookies.delete(cookies_config.COOKIES_KEY)

    response: Response = await async_client.get(url=RouterConfig.PREFIX + URLPathsConfig.MY_STATS)

    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert get_error_message_from_response(response=response) == ErrorDetails.USER_NOT_AUTHENTICATED
