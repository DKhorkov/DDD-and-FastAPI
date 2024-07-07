import pytest
from fastapi import status
from httpx import Response, AsyncClient

from src.users.config import RouterConfig, URLPathsConfig, UserValidationConfig
from src.users.constants import ErrorDetails
from src.users.models import UserModel
from tests.utils import get_error_message_from_response, generate_random_string
from tests.config import FakeUserConfig


@pytest.mark.anyio
async def test_register_fail_incorrect_email_pattern(async_client: AsyncClient) -> None:
    test_user_config: FakeUserConfig = FakeUserConfig()
    test_user_config.EMAIL = '<EMAIL>'
    response: Response = await async_client.post(
        url=RouterConfig.PREFIX + URLPathsConfig.REGISTER,
        json=test_user_config.to_dict(to_lower=True)
    )

    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

    expected_error_message: str = ('value is not a valid email address: '
                                   'An email address must have an @-sign.')
    assert get_error_message_from_response(response=response) == expected_error_message


@pytest.mark.anyio
async def test_register_fail_too_short_username(async_client: AsyncClient) -> None:
    test_user_config: FakeUserConfig = FakeUserConfig()
    test_user_config.USERNAME = generate_random_string(length=UserValidationConfig.USERNAME_MIN_LENGTH - 1)
    response: Response = await async_client.post(
        url=RouterConfig.PREFIX + URLPathsConfig.REGISTER,
        json=test_user_config.to_dict(to_lower=True)
    )

    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    assert get_error_message_from_response(response=response) == ErrorDetails.USERNAME_VALIDATION_ERROR


@pytest.mark.anyio
async def test_register_fail_too_long_username(async_client: AsyncClient) -> None:
    test_user_config: FakeUserConfig = FakeUserConfig()
    test_user_config.USERNAME = generate_random_string(length=UserValidationConfig.USERNAME_MAX_LENGTH + 1)
    response: Response = await async_client.post(
        url=RouterConfig.PREFIX + URLPathsConfig.REGISTER,
        json=test_user_config.to_dict(to_lower=True)
    )

    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    assert get_error_message_from_response(response=response) == ErrorDetails.USERNAME_VALIDATION_ERROR


@pytest.mark.anyio
async def test_register_fail_too_short_password(async_client: AsyncClient) -> None:
    test_user_config: FakeUserConfig = FakeUserConfig()
    test_user_config.PASSWORD = generate_random_string(length=UserValidationConfig.PASSWORD_MIN_LENGTH - 1)
    response: Response = await async_client.post(
        url=RouterConfig.PREFIX + URLPathsConfig.REGISTER,
        json=test_user_config.to_dict(to_lower=True)
    )

    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    assert get_error_message_from_response(response=response) == ErrorDetails.PASSWORD_VALIDATION_ERROR


@pytest.mark.anyio
async def test_register_fail_too_long_password(async_client: AsyncClient) -> None:
    test_user_config: FakeUserConfig = FakeUserConfig()
    test_user_config.PASSWORD = generate_random_string(length=UserValidationConfig.PASSWORD_MAX_LENGTH + 1)
    response: Response = await async_client.post(
        url=RouterConfig.PREFIX + URLPathsConfig.REGISTER,
        json=test_user_config.to_dict(to_lower=True)
    )

    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    assert get_error_message_from_response(response=response) == ErrorDetails.PASSWORD_VALIDATION_ERROR


@pytest.mark.anyio
async def test_register_success(async_client: AsyncClient) -> None:
    response: Response = await async_client.post(
        url=RouterConfig.PREFIX + URLPathsConfig.REGISTER,
        json=FakeUserConfig().to_dict(to_lower=True)
    )

    assert response.status_code == status.HTTP_201_CREATED
    user: UserModel = UserModel(**response.json())
    assert user.email == FakeUserConfig.EMAIL
    assert user.username == FakeUserConfig.USERNAME


@pytest.mark.anyio
async def test_register_fail_email_already_taken(
        async_client: AsyncClient,
        create_test_user: None
) -> None:

    test_user_config: FakeUserConfig = FakeUserConfig()
    test_user_config.USERNAME = 'some_new_username'
    response: Response = await async_client.post(
        url=RouterConfig.PREFIX + URLPathsConfig.REGISTER,
        json=test_user_config.to_dict(to_lower=True)
    )

    assert response.status_code == status.HTTP_409_CONFLICT
    assert get_error_message_from_response(response=response) == ErrorDetails.USER_ALREADY_EXISTS


@pytest.mark.anyio
async def test_register_fail_username_already_taken(
        async_client: AsyncClient,
        create_test_user: None
) -> None:

    test_user_config: FakeUserConfig = FakeUserConfig()
    test_user_config.EMAIL = 'some_new_email@mail.ru'
    response: Response = await async_client.post(
        url=RouterConfig.PREFIX + URLPathsConfig.REGISTER,
        json=test_user_config.to_dict(to_lower=True)
    )

    assert response.status_code == status.HTTP_409_CONFLICT
    assert get_error_message_from_response(response=response) == ErrorDetails.USER_ALREADY_EXISTS
