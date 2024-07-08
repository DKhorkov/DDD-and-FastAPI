import pytest
from fastapi import status
from httpx import Response, AsyncClient, Cookies
from typing import Dict, Any, Optional
from sqlalchemy import insert, CursorResult, RowMapping
from sqlalchemy.ext.asyncio import AsyncConnection

from src.users.domain.models import UserModel, UserStatisticsModel
from src.core.utils import get_substring_before_chars, get_substring_after_chars
from src.users.config import RouterConfig, URLPathsConfig, cookies_config
from src.users.constants import ErrorDetails
from tests.utils import get_error_message_from_response


@pytest.mark.anyio
async def test_dislike_user_success(
        async_client: AsyncClient,
        create_test_user: None,
        cookies: Cookies,
        async_connection: AsyncConnection
) -> None:

    cursor: CursorResult = await async_connection.execute(
        insert(
            UserModel
        ).values(
            email='second_user_email',
            password='<PASSWORD>',
            username='second_user_username',
        ).returning(
            UserModel
        )
    )
    user_data: Optional[RowMapping] = cursor.mappings().fetchone()
    assert user_data is not None
    user: UserModel = UserModel(**user_data)
    await async_connection.execute(insert(UserStatisticsModel).values(user_id=user.id))
    await async_connection.commit()

    dislike_user_url_prefix: str = get_substring_before_chars(
        chars='{',
        string=URLPathsConfig.DISLIKE_USER
    )

    dislike_user_url_postfix: str = get_substring_after_chars(
        chars='}',
        string=URLPathsConfig.DISLIKE_USER
    )

    response: Response = await async_client.patch(
        url=RouterConfig.PREFIX + dislike_user_url_prefix + '2' + dislike_user_url_postfix,
        cookies=cookies
    )

    assert response.status_code == status.HTTP_200_OK

    response_content: Dict[str, Any] = response.json()
    assert response_content['likes'] == 0
    assert response_content['dislikes'] == 1


@pytest.mark.anyio
async def test_dislike_user_fail_user_not_authorized(async_client: AsyncClient, create_test_user: None) -> None:
    # Deleting cookies from async client, because if used as a "session" fixture:
    async_client.cookies.delete(cookies_config.COOKIES_KEY)

    dislike_user_url_prefix: str = get_substring_before_chars(
        chars='{',
        string=URLPathsConfig.DISLIKE_USER
    )

    dislike_user_url_postfix: str = get_substring_after_chars(
        chars='}',
        string=URLPathsConfig.DISLIKE_USER
    )

    response: Response = await async_client.patch(
        url=RouterConfig.PREFIX + dislike_user_url_prefix + '2' + dislike_user_url_postfix,
    )

    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert get_error_message_from_response(response=response) == ErrorDetails.USER_NOT_AUTHENTICATED


@pytest.mark.anyio
async def test_dislike_user_fail_voted_for_user_does_not_exists(
        async_client: AsyncClient,
        create_test_user: None,
        cookies: Cookies
) -> None:

    dislike_user_url_prefix: str = get_substring_before_chars(
        chars='{',
        string=URLPathsConfig.DISLIKE_USER
    )

    dislike_user_url_postfix: str = get_substring_after_chars(
        chars='}',
        string=URLPathsConfig.DISLIKE_USER
    )

    response: Response = await async_client.patch(
        url=RouterConfig.PREFIX + dislike_user_url_prefix + '2' + dislike_user_url_postfix,
        cookies=cookies
    )

    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert get_error_message_from_response(response=response) == ErrorDetails.USER_STATISTICS_NOT_FOUND


@pytest.mark.anyio
async def test_dislike_user_fail_user_can_not_vote_for_himself(
        async_client: AsyncClient,
        create_test_user: None,
        cookies: Cookies
) -> None:

    dislike_user_url_prefix: str = get_substring_before_chars(
        chars='{',
        string=URLPathsConfig.DISLIKE_USER
    )

    dislike_user_url_postfix: str = get_substring_after_chars(
        chars='}',
        string=URLPathsConfig.DISLIKE_USER
    )

    response: Response = await async_client.patch(
        url=RouterConfig.PREFIX + dislike_user_url_prefix + '1' + dislike_user_url_postfix,
        cookies=cookies
    )

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert get_error_message_from_response(response=response) == ErrorDetails.USER_CAN_NOT_VOTE_FOR_HIMSELF


@pytest.mark.anyio
async def test_dislike_user_fail_can_not_vote_more_than_one_time(
        async_client: AsyncClient,
        create_test_user: None,
        cookies: Cookies,
        async_connection: AsyncConnection
) -> None:
    cursor: CursorResult = await async_connection.execute(
        insert(
            UserModel
        ).values(
            email='second_user_email',
            password='<PASSWORD>',
            username='second_user_username',
        ).returning(
            UserModel
        )
    )
    user_data: Optional[RowMapping] = cursor.mappings().fetchone()
    assert user_data is not None
    user: UserModel = UserModel(**user_data)
    await async_connection.execute(insert(UserStatisticsModel).values(user_id=user.id))
    await async_connection.commit()

    dislike_user_url_prefix: str = get_substring_before_chars(
        chars='{',
        string=URLPathsConfig.DISLIKE_USER
    )

    dislike_user_url_postfix: str = get_substring_after_chars(
        chars='}',
        string=URLPathsConfig.DISLIKE_USER
    )

    response: Response = await async_client.patch(
        url=RouterConfig.PREFIX + dislike_user_url_prefix + '2' + dislike_user_url_postfix,
        cookies=cookies
    )

    assert response.status_code == status.HTTP_200_OK

    response_content: Dict[str, Any] = response.json()
    assert response_content['likes'] == 0
    assert response_content['dislikes'] == 1

    response = await async_client.patch(
        url=RouterConfig.PREFIX + dislike_user_url_prefix + '2' + dislike_user_url_postfix,
        cookies=cookies
    )

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert get_error_message_from_response(response=response) == ErrorDetails.USER_ALREADY_VOTED
