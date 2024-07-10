import pytest
from datetime import datetime, timezone
from typing import List, Optional

from sqlalchemy import insert, RowMapping, CursorResult
from sqlalchemy.ext.asyncio import AsyncConnection

from src.users.exceptions import (
    UserAlreadyExistsError,
    InvalidPasswordError,
    UserNotFoundError,
    UserCanNotVoteForHimSelf,
    UserAlreadyVotedError,
    UserStatisticsNotFoundError,
)
from src.security.exceptions import InvalidTokenError
from src.users.models import UserModel, UserStatisticsModel
from src.security.models import JWTDataModel
from src.users.schemas import RegisterUserScheme, LoginUserScheme
from src.security.utils import create_jwt_token
from tests.config import FakeUserConfig
from src.users.dependencies import (
    register_user,
    authenticate_user,
    verify_user_credentials,
    get_all_users,
    dislike_user,
    like_user,
    get_my_statistics
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
async def test_authenticate_user_success(create_test_db: None, access_token: str) -> None:
    user: UserModel = await authenticate_user(token=access_token)
    assert user.email == FakeUserConfig.EMAIL
    assert user.username == FakeUserConfig.USERNAME


@pytest.mark.anyio
async def test_authenticate_user_fail_invalid_token(create_test_db: None) -> None:
    with pytest.raises(InvalidTokenError):
        await authenticate_user(token='someInvalidToken')


@pytest.mark.anyio
async def test_authenticate_user_fail_token_expired(create_test_db: None) -> None:
    jwt_data: JWTDataModel = JWTDataModel(user_id=1, exp=datetime.now(timezone.utc))
    token: str = await create_jwt_token(jwt_data=jwt_data)
    with pytest.raises(InvalidTokenError):
        await authenticate_user(token=token)


@pytest.mark.anyio
async def test_authenticate_user_fail_user_does_not_exist(create_test_db: None) -> None:
    jwt_data: JWTDataModel = JWTDataModel(user_id=1)
    token: str = await create_jwt_token(jwt_data=jwt_data)
    with pytest.raises(UserNotFoundError):
        await authenticate_user(token=token)


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
async def test_get_my_statistics_success(create_test_user: None) -> None:
    statistics: UserStatisticsModel = await get_my_statistics(
        user=UserModel(
            id=1,
            **FakeUserConfig().to_dict(to_lower=True)
        )
    )
    assert statistics.likes == 0
    assert statistics.dislikes == 0


@pytest.mark.anyio
async def test_get_my_statistics_fail_user_does_not_exist(create_test_db: None) -> None:
    with pytest.raises(UserStatisticsNotFoundError):
        await get_my_statistics(
            user=UserModel(
                id=1,
                **FakeUserConfig().to_dict(to_lower=True)
            )
        )


@pytest.mark.anyio
async def test_like_user_success(create_test_user: None, async_connection: AsyncConnection) -> None:
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
        user=UserModel(
            id=1,
            **FakeUserConfig().to_dict(to_lower=True)
        )
    )
    assert statistics.likes == 1
    assert statistics.dislikes == 0


@pytest.mark.anyio
async def test_like_user_fail_can_not_vote_more_than_one_time(
        create_test_user: None,
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
        user=UserModel(
            id=1,
            **FakeUserConfig().to_dict(to_lower=True)
        )
    )

    with pytest.raises(UserAlreadyVotedError):
        await like_user(
            user_id=user.id,
            user=UserModel(
                id=1,
                **FakeUserConfig().to_dict(to_lower=True)
            )
        )


@pytest.mark.anyio
async def test_like_user_fail_can_not_for_himself(create_test_user: None) -> None:
    with pytest.raises(UserCanNotVoteForHimSelf):
        await like_user(
            user_id=1,
            user=UserModel(
                id=1,
                **FakeUserConfig().to_dict(to_lower=True)
            )
        )


@pytest.mark.anyio
async def test_dislike_user_success(create_test_user: None, async_connection: AsyncConnection) -> None:
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
        user=UserModel(
            id=1,
            **FakeUserConfig().to_dict(to_lower=True)
        )
    )
    assert statistics.likes == 0
    assert statistics.dislikes == 1


@pytest.mark.anyio
async def test_dislike_user_fail_can_not_vote_more_than_one_time(
        create_test_user: None,
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
        user=UserModel(
            id=1,
            **FakeUserConfig().to_dict(to_lower=True)
        )
    )

    with pytest.raises(UserAlreadyVotedError):
        await dislike_user(
            user_id=user.id,
            user=UserModel(
                id=1,
                **FakeUserConfig().to_dict(to_lower=True)
            )
        )


@pytest.mark.anyio
async def test_dislike_user_fail_can_not_for_himself(create_test_user: None) -> None:
    with pytest.raises(UserCanNotVoteForHimSelf):
        await dislike_user(
            user_id=1,
            user=UserModel(
                id=1,
                **FakeUserConfig().to_dict(to_lower=True)
            )
        )
