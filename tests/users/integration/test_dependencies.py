import pytest
from typing import List, Optional
from sqlalchemy import CursorResult, insert, RowMapping
from sqlalchemy.ext.asyncio import AsyncConnection

from src.users.exceptions import (
    UserAlreadyExistsError,
    InvalidPasswordError,
    UserNotFoundError,
    UserStatisticsNotFoundError,
    UserAlreadyVotedError,
    UserCanNotVoteForHimSelf
)
from src.users.domain.models import UserModel, UserStatisticsModel
from src.users.entrypoints.schemas import RegisterUserScheme, LoginUserScheme
from tests.config import FakeUserConfig
from src.users.entrypoints.dependencies import (
    register_user,
    verify_user_credentials,
    get_all_users,
    get_my_statistics,
    like_user,
    dislike_user
)


@pytest.mark.anyio
async def test_register_user_success(create_test_db: None) -> None:
    user_data: RegisterUserScheme = RegisterUserScheme(**FakeUserConfig().to_dict(to_lower=True))
    user: UserModel = await register_user(user_data=user_data)

    assert user.id == 1
    assert user.username == FakeUserConfig.USERNAME
    assert user.email == FakeUserConfig.EMAIL


@pytest.mark.anyio
async def test_register_user_fail(create_test_user: None) -> None:
    user_data: RegisterUserScheme = RegisterUserScheme(**FakeUserConfig().to_dict(to_lower=True))
    with pytest.raises(UserAlreadyExistsError):
        await register_user(user_data=user_data)


@pytest.mark.anyio
async def test_verify_user_credentials_by_username_success(create_test_user: None) -> None:
    user_data: LoginUserScheme = LoginUserScheme(username=FakeUserConfig.USERNAME, password=FakeUserConfig.PASSWORD)
    user: UserModel = await verify_user_credentials(user_data=user_data)

    assert user.id == 1
    assert user.username == FakeUserConfig.USERNAME
    assert user.email == FakeUserConfig.EMAIL


@pytest.mark.anyio
async def test_verify_user_credentials_by_email_success(create_test_user: None) -> None:
    user_data: LoginUserScheme = LoginUserScheme(username=FakeUserConfig.EMAIL, password=FakeUserConfig.PASSWORD)
    user: UserModel = await verify_user_credentials(user_data=user_data)

    assert user.id == 1
    assert user.username == FakeUserConfig.USERNAME
    assert user.email == FakeUserConfig.EMAIL


@pytest.mark.anyio
async def test_verify_user_credentials_fail_user_does_not_exist(create_test_db: None) -> None:
    user_data: LoginUserScheme = LoginUserScheme(**FakeUserConfig().to_dict(to_lower=True))
    with pytest.raises(UserNotFoundError):
        await verify_user_credentials(user_data=user_data)


@pytest.mark.anyio
async def test_verify_user_credentials_fail_incorrect_password(create_test_user: None) -> None:
    user_data: LoginUserScheme = LoginUserScheme(**FakeUserConfig().to_dict(to_lower=True))
    user_data.password = 'some_incorrect_password'
    with pytest.raises(InvalidPasswordError):
        await verify_user_credentials(user_data=user_data)


@pytest.mark.anyio
async def test_get_all_users_with_existing_user(create_test_user: None) -> None:
    users: List[UserModel] = await get_all_users()
    assert len(users) == 1
    user: UserModel = users[0]
    assert user.id == 1
    assert user.username == FakeUserConfig.USERNAME
    assert user.email == FakeUserConfig.EMAIL


@pytest.mark.anyio
async def test_get_all_users_without_existing_users(create_test_db: None) -> None:
    users: List[UserModel] = await get_all_users()
    assert len(users) == 0


@pytest.mark.anyio
async def test_get_my_statistics_success(access_token: str) -> None:
    statistics: UserStatisticsModel = await get_my_statistics(token=access_token)
    assert statistics.likes == 0
    assert statistics.dislikes == 0


@pytest.mark.anyio
async def test_get_my_statistics_fail_user_does_not_exist(map_models_to_orm: None) -> None:
    with pytest.raises(UserStatisticsNotFoundError):
        await get_my_statistics(
            token='eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoyLCJleHAiOjE3MjM2NDc4Mjl9.'
                  'vrltPl_1Bh2LSsvjAd3S7N2ylUX4UzT1q2rrO76M3UI'
        )


@pytest.mark.anyio
async def test_like_user_success(access_token: str, async_connection: AsyncConnection) -> None:
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

    statistics: UserStatisticsModel = await like_user(
        user_id=user.id,
        token=access_token
    )
    assert statistics.likes == 1
    assert statistics.dislikes == 0


@pytest.mark.anyio
async def test_like_user_fail_can_not_vote_more_than_one_time(
        access_token: str,
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

    await like_user(
        user_id=user.id,
        token=access_token
    )

    with pytest.raises(UserAlreadyVotedError):
        await like_user(
            user_id=user.id,
            token=access_token
        )


@pytest.mark.anyio
async def test_like_user_fail_can_not_for_himself(access_token: str) -> None:
    with pytest.raises(UserCanNotVoteForHimSelf):
        await like_user(
            user_id=1,
            token=access_token
        )


@pytest.mark.anyio
async def test_dislike_user_success(access_token: str, async_connection: AsyncConnection) -> None:
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

    statistics: UserStatisticsModel = await dislike_user(
        user_id=user.id,
        token=access_token
    )
    assert statistics.likes == 0
    assert statistics.dislikes == 1


@pytest.mark.anyio
async def test_dislike_user_fail_can_not_vote_more_than_one_time(
        access_token: str,
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

    await dislike_user(
        user_id=user.id,
        token=access_token
    )

    with pytest.raises(UserAlreadyVotedError):
        await dislike_user(
            user_id=user.id,
            token=access_token
        )


@pytest.mark.anyio
async def test_dislike_user_fail_can_not_for_himself(access_token: str) -> None:
    with pytest.raises(UserCanNotVoteForHimSelf):
        await dislike_user(
            user_id=1,
            token=access_token
        )
