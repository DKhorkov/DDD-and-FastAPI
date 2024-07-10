import pytest
from typing import Optional, List
from sqlalchemy import select, insert, CursorResult, Row
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncConnection

from src.users.constants import ErrorDetails
from src.users.exceptions import UserNotFoundError, UserStatisticsNotFoundError
from src.users.service import UsersService
from src.users.models import UserModel, UserStatisticsModel, UserVoteModel
from tests.config import FakeUserConfig


@pytest.mark.anyio
async def test_users_service_get_user_by_id_success(create_test_user: None) -> None:
    user: Optional[UserModel] = await UsersService().get_user_by_id(id=1)

    assert user is not None
    assert user.id == 1
    assert user.email == FakeUserConfig.EMAIL
    assert user.username == FakeUserConfig.USERNAME


@pytest.mark.anyio
async def test_users_service_get_user_by_id_fail(create_test_db: None) -> None:
    with pytest.raises(UserNotFoundError):
        await UsersService().get_user_by_id(id=1)


@pytest.mark.anyio
async def test_users_service_get_user_by_email_success(create_test_user: None) -> None:
    user: Optional[UserModel] = await UsersService().get_user_by_email(
        email=FakeUserConfig.EMAIL
    )

    assert user is not None
    assert user.id == 1
    assert user.email == FakeUserConfig.EMAIL
    assert user.username == FakeUserConfig.USERNAME


@pytest.mark.anyio
async def test_users_service_get_user_by_email_fail(create_test_db: None) -> None:
    with pytest.raises(UserNotFoundError):
        await UsersService().get_user_by_email(email=FakeUserConfig.EMAIL)


@pytest.mark.anyio
async def test_users_service_get_user_by_username_success(create_test_user: None) -> None:
    user: Optional[UserModel] = await UsersService().get_user_by_username(
        username=FakeUserConfig.USERNAME
    )

    assert user is not None
    assert user.id == 1
    assert user.email == FakeUserConfig.EMAIL
    assert user.username == FakeUserConfig.USERNAME


@pytest.mark.anyio
async def test_users_service_get_user_by_username_fail(create_test_db: None) -> None:
    with pytest.raises(UserNotFoundError):
        await UsersService().get_user_by_username(username=FakeUserConfig.USERNAME)


@pytest.mark.anyio
async def test_users_service_get_all_users_with_existing_users(create_test_user: None) -> None:
    users_list: List[UserModel] = await UsersService().get_all_users()
    assert len(users_list) == 1

    user: UserModel = users_list[0]
    assert user.id == 1
    assert user.email == FakeUserConfig.EMAIL
    assert user.username == FakeUserConfig.USERNAME


@pytest.mark.anyio
async def test_users_service_get_all_users_without_existing_users(create_test_db: None) -> None:
    users_list: List[UserModel] = await UsersService().get_all_users()
    assert len(users_list) == 0


@pytest.mark.anyio
async def test_users_service_register_user_success(
        create_test_db: None,
        async_connection: AsyncConnection
) -> None:

    cursor: CursorResult = await async_connection.execute(select(UserModel).filter_by(email=FakeUserConfig.EMAIL))
    result: Optional[Row] = cursor.first()
    assert not result

    user: UserModel = UserModel(**FakeUserConfig().to_dict(to_lower=True))
    user = await UsersService().register_user(user=user)
    assert user.id == 1
    assert user.email == FakeUserConfig.EMAIL
    assert user.username == FakeUserConfig.USERNAME

    cursor = await async_connection.execute(select(UserModel).filter_by(email=FakeUserConfig.EMAIL))
    result = cursor.first()
    assert result

    cursor = await async_connection.execute(select(UserStatisticsModel).filter_by(user_id=1))
    result = cursor.first()
    assert result


@pytest.mark.anyio
async def test_users_service_register_user_fail_username_already_exists(
        create_test_user: None,
        async_connection: AsyncConnection
) -> None:

    cursor: CursorResult = await async_connection.execute(select(UserModel).filter_by(username=FakeUserConfig.USERNAME))
    result: Optional[Row] = cursor.first()
    assert result

    user: UserModel = UserModel(
        username=FakeUserConfig.USERNAME,
        email='someTestEmail@gmail.com',
        password=FakeUserConfig.PASSWORD
    )

    with pytest.raises(IntegrityError):
        await UsersService().register_user(user=user)


@pytest.mark.anyio
async def test_users_service_register_user_fail_email_already_exists(
        create_test_user: None,
        async_connection: AsyncConnection
) -> None:

    cursor: CursorResult = await async_connection.execute(select(UserModel).filter_by(email=FakeUserConfig.EMAIL))
    result: Optional[Row] = cursor.first()
    assert result

    user: UserModel = UserModel(
        email=FakeUserConfig.EMAIL,
        username='someUsername',
        password=FakeUserConfig.PASSWORD
    )

    with pytest.raises(IntegrityError):
        await UsersService().register_user(user=user)


@pytest.mark.anyio
async def test_users_service_check_user_existence_success_by_id(create_test_user: None) -> None:
    assert await UsersService().check_user_existence(id=1)


@pytest.mark.anyio
async def test_users_service_check_user_existence_success_by_email(create_test_user: None) -> None:
    assert await UsersService().check_user_existence(email=FakeUserConfig.EMAIL)


@pytest.mark.anyio
async def test_users_service_check_user_existence_success_by_username(create_test_user: None) -> None:
    assert await UsersService().check_user_existence(username=FakeUserConfig.USERNAME)


@pytest.mark.anyio
async def test_users_service_check_user_existence_fail_user_does_not_exist(create_test_db: None) -> None:
    assert not await UsersService().check_user_existence(username=FakeUserConfig.USERNAME)


@pytest.mark.anyio
async def test_users_service_check_user_existence_fail_no_attributes_provided(create_test_db: None) -> None:
    with pytest.raises(ValueError) as exc_info:
        await UsersService().check_user_existence()

    assert str(exc_info.value) == ErrorDetails.USER_ATTRIBUTE_REQUIRED


@pytest.mark.anyio
async def test_get_user_statistics_by_user_id_success(create_test_user: None) -> None:
    user_statistics: UserStatisticsModel = await UsersService().get_user_statistics_by_user_id(user_id=1)
    assert user_statistics.likes == 0
    assert user_statistics.dislikes == 0


@pytest.mark.anyio
async def test_get_user_statistics_by_user_id_fail_user_statistics_not_found(create_test_db: None) -> None:
    with pytest.raises(UserStatisticsNotFoundError):
        await UsersService().get_user_statistics_by_user_id(user_id=1)


@pytest.mark.anyio
async def test_like_user_success(create_test_user: None) -> None:
    user_statistics: UserStatisticsModel = await UsersService().like_user(voting_user_id=1, voted_for_user_id=1)
    assert user_statistics.likes == 1
    assert user_statistics.dislikes == 0


@pytest.mark.anyio
async def test_like_user_fail_user_statistics_not_found(create_test_db: None) -> None:
    with pytest.raises(UserStatisticsNotFoundError):
        await UsersService().like_user(voting_user_id=1, voted_for_user_id=1)


@pytest.mark.anyio
async def test_dislike_user_success(create_test_user: None) -> None:
    user_statistics: UserStatisticsModel = await UsersService().dislike_user(voting_user_id=1, voted_for_user_id=1)
    assert user_statistics.likes == 0
    assert user_statistics.dislikes == 1


@pytest.mark.anyio
async def test_dislike_user_fail_user_statistics_not_found(create_test_db: None) -> None:
    with pytest.raises(UserStatisticsNotFoundError):
        await UsersService().dislike_user(voting_user_id=1, voted_for_user_id=1)


@pytest.mark.anyio
async def test_check_if_user_already_voted_success(create_test_user: None, async_connection: AsyncConnection) -> None:
    await async_connection.execute(
        insert(
            UserVoteModel
        ).values(
            voted_for_user_id=1,
            voting_user_id=1
        )
    )
    await async_connection.commit()

    assert await UsersService().check_if_user_already_voted(voting_user_id=1, voted_for_user_id=1)


@pytest.mark.anyio
async def test_check_if_user_already_voted_fail(create_test_db: None) -> None:
    assert not await UsersService().check_if_user_already_voted(voting_user_id=1, voted_for_user_id=1)
