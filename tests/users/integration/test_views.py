import pytest
from typing import List

from src.users.domain.models import UserModel
from src.users.exceptions import UserNotFoundError
from src.users.interfaces import UsersUnitOfWork, UsersRepository
from src.users.entrypoints.views import UsersViews
from tests.config import FakeUserConfig
from tests.users.fake_objects import FakeUsersUnitOfWork
from tests.users.utils import create_fake_users_repository_instance


@pytest.mark.anyio
async def test_users_views_get_user_account_success() -> None:
    users_repository: UsersRepository = await create_fake_users_repository_instance(with_user=True)
    users_unit_of_work: UsersUnitOfWork = FakeUsersUnitOfWork(users_repository=users_repository)
    user: UserModel = await UsersViews(uow=users_unit_of_work).get_user_account(user_id=1)
    assert user.email == FakeUserConfig.EMAIL
    assert user.username == FakeUserConfig.USERNAME
    assert not user.password


@pytest.mark.anyio
async def test_users_views_get_user_account_fails_user_does_not_exist() -> None:
    users_repository: UsersRepository = await create_fake_users_repository_instance()
    users_unit_of_work: UsersUnitOfWork = FakeUsersUnitOfWork(users_repository=users_repository)
    with pytest.raises(UserNotFoundError):
        await UsersViews(uow=users_unit_of_work).get_user_account(user_id=1)


@pytest.mark.anyio
async def test_users_views_get_all_users_with_existing_users() -> None:
    users_repository: UsersRepository = await create_fake_users_repository_instance(with_user=True)
    users_unit_of_work: UsersUnitOfWork = FakeUsersUnitOfWork(users_repository=users_repository)
    users: List[UserModel] = await UsersViews(uow=users_unit_of_work).get_all_users()
    assert len(users) == 1
    user: UserModel = users[0]
    assert user.email == FakeUserConfig.EMAIL
    assert user.username == FakeUserConfig.USERNAME
    assert not user.password


@pytest.mark.anyio
async def test_users_views_get_all_users_without_existing_users() -> None:
    users_repository: UsersRepository = await create_fake_users_repository_instance()
    users_unit_of_work: UsersUnitOfWork = FakeUsersUnitOfWork(users_repository=users_repository)
    users: List[UserModel] = await UsersViews(uow=users_unit_of_work).get_all_users()
    assert len(users) == 0
