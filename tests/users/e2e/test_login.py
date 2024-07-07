import pytest
from fastapi import status
from httpx import Response, AsyncClient

from src.users.config import RouterConfig, URLPathsConfig, cookies_config
from src.users.constants import ErrorDetails
from tests.config import FakeUserConfig
from tests.utils import get_error_message_from_response


@pytest.mark.anyio
async def test_login_by_email_success(async_client: AsyncClient, create_test_user: None) -> None:
    response: Response = await async_client.post(
        url=RouterConfig.PREFIX + URLPathsConfig.LOGIN,
        json={
            'username': FakeUserConfig.EMAIL,
            'password': FakeUserConfig.PASSWORD
        }
    )

    assert response.status_code == status.HTTP_200_OK
    assert response.cookies.get(cookies_config.COOKIES_KEY)


@pytest.mark.anyio
async def test_login_by_username_success(async_client: AsyncClient, create_test_user: None) -> None:
    response: Response = await async_client.post(
        url=RouterConfig.PREFIX + URLPathsConfig.LOGIN,
        json={
            'username': FakeUserConfig.USERNAME,
            'password': FakeUserConfig.PASSWORD
        }
    )

    assert response.status_code == status.HTTP_200_OK
    assert response.cookies.get(cookies_config.COOKIES_KEY)


@pytest.mark.anyio
async def test_login_fail_user_not_found(async_client: AsyncClient, create_test_db: None) -> None:
    response: Response = await async_client.post(
        url=RouterConfig.PREFIX + URLPathsConfig.LOGIN,
        json=FakeUserConfig().to_dict(to_lower=True)
    )

    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert get_error_message_from_response(response=response) == ErrorDetails.USER_NOT_FOUND


@pytest.mark.anyio
async def test_login_fail_incorrect_password(async_client: AsyncClient, create_test_user: None) -> None:
    test_user_config: FakeUserConfig = FakeUserConfig()
    test_user_config.PASSWORD = 'incorrectPassword'
    response: Response = await async_client.post(
        url=RouterConfig.PREFIX + URLPathsConfig.LOGIN,
        json=test_user_config.to_dict(to_lower=True)
    )

    assert response.status_code == status.HTTP_412_PRECONDITION_FAILED
    assert get_error_message_from_response(response=response) == ErrorDetails.INVALID_PASSWORD
