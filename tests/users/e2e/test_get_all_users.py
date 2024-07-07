import pytest
from fastapi import status
from httpx import Response, AsyncClient
from typing import Dict, Any, List

from src.users.config import RouterConfig, URLPathsConfig
from tests.config import FakeUserConfig


@pytest.mark.anyio
async def test_get_all_users_with_existing_user(
        async_client: AsyncClient,
        create_test_user: None,
) -> None:

    response: Response = await async_client.get(url=RouterConfig.PREFIX + URLPathsConfig.ALL)
    assert response.status_code == status.HTTP_200_OK

    response_content: List[Dict[str, Any]] = response.json()
    assert len(response_content) == 1
    user: Dict[str, Any] = response_content[0]
    assert user['id'] == 1
    assert user['email'] == FakeUserConfig.EMAIL
    assert user['username'] == FakeUserConfig.USERNAME


@pytest.mark.anyio
async def test_get_all_users_without_existing_users(async_client: AsyncClient, create_test_db: None) -> None:
    response: Response = await async_client.get(url=RouterConfig.PREFIX + URLPathsConfig.ALL)
    assert response.status_code == status.HTTP_200_OK

    response_content: List[Dict[str, Any]] = response.json()
    assert len(response_content) == 0
