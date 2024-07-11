import pytest
from typing import List

from src.users.constants import ErrorDetails
from src.users.exceptions import UserNotFoundError, UserStatisticsNotFoundError
from src.users.interfaces.repositories import UsersRepository, UsersStatisticsRepository
from src.users.interfaces.units_of_work import UsersUnitOfWork
from src.users.domain.models import UserModel, UserStatisticsModel, UserVoteModel
from src.users.service import UsersService
from tests.users.fake_objects import FakeUsersUnitOfWork, FakeUsersVotesRepository
from tests.config import FakeUserConfig
from tests.users.utils import create_fake_users_repository_instance, create_fake_users_statistics_repository_instance


@pytest.mark.anyio
async def test_users_service_register_user_success() -> None:
    users_repository: UsersRepository = await create_fake_users_repository_instance()
    users_statistics_repository: UsersStatisticsRepository = await create_fake_users_statistics_repository_instance()
    users_unit_of_work: UsersUnitOfWork = FakeUsersUnitOfWork(
        users_repository=users_repository,
        users_statistics_repository=users_statistics_repository,
        users_votes_repository=FakeUsersVotesRepository()
    )
    users_service: UsersService = UsersService(uow=users_unit_of_work)

    assert len(await users_repository.list()) == 0
    user: UserModel = UserModel(**FakeUserConfig().to_dict(to_lower=True))
    await users_service.register_user(user=user)
    assert len(await users_repository.list()) == 1
    assert len(await users_statistics_repository.list()) == 1


@pytest.mark.anyio
async def test_users_service_get_user_by_id_success() -> None:
    users_repository: UsersRepository = await create_fake_users_repository_instance(with_user=True)
    users_statistics_repository: UsersStatisticsRepository = await create_fake_users_statistics_repository_instance(
        with_user=True
    )
    users_unit_of_work: UsersUnitOfWork = FakeUsersUnitOfWork(
        users_repository=users_repository,
        users_statistics_repository=users_statistics_repository,
        users_votes_repository=FakeUsersVotesRepository()
    )
    users_service: UsersService = UsersService(uow=users_unit_of_work)

    assert len(await users_repository.list()) == 1
    found_user: UserModel = await users_service.get_user_by_id(id=1)
    assert found_user.email == FakeUserConfig.EMAIL
    assert found_user.username == FakeUserConfig.USERNAME
    assert found_user.id == 1


@pytest.mark.anyio
async def test_users_service_get_user_by_id_fail() -> None:
    users_repository: UsersRepository = await create_fake_users_repository_instance()
    users_statistics_repository: UsersStatisticsRepository = await create_fake_users_statistics_repository_instance()
    users_unit_of_work: UsersUnitOfWork = FakeUsersUnitOfWork(
        users_repository=users_repository,
        users_statistics_repository=users_statistics_repository,
        users_votes_repository=FakeUsersVotesRepository()
    )
    users_service: UsersService = UsersService(uow=users_unit_of_work)

    assert len(await users_repository.list()) == 0
    with pytest.raises(UserNotFoundError):
        await users_service.get_user_by_id(id=1)


@pytest.mark.anyio
async def test_users_service_get_user_by_email_success() -> None:
    users_repository: UsersRepository = await create_fake_users_repository_instance(with_user=True)
    users_statistics_repository: UsersStatisticsRepository = await create_fake_users_statistics_repository_instance(
        with_user=True
    )
    users_unit_of_work: UsersUnitOfWork = FakeUsersUnitOfWork(
        users_repository=users_repository,
        users_statistics_repository=users_statistics_repository,
        users_votes_repository=FakeUsersVotesRepository()
    )
    users_service: UsersService = UsersService(uow=users_unit_of_work)

    assert len(await users_repository.list()) == 1
    found_user: UserModel = await users_service.get_user_by_email(email=FakeUserConfig.EMAIL)
    assert found_user.email == FakeUserConfig.EMAIL
    assert found_user.username == FakeUserConfig.USERNAME
    assert found_user.id == 1


@pytest.mark.anyio
async def test_users_service_get_user_by_email_fail() -> None:
    users_repository: UsersRepository = await create_fake_users_repository_instance()
    users_statistics_repository: UsersStatisticsRepository = await create_fake_users_statistics_repository_instance()
    users_unit_of_work: UsersUnitOfWork = FakeUsersUnitOfWork(
        users_repository=users_repository,
        users_statistics_repository=users_statistics_repository,
        users_votes_repository=FakeUsersVotesRepository()
    )
    users_service: UsersService = UsersService(uow=users_unit_of_work)

    assert len(await users_repository.list()) == 0
    with pytest.raises(UserNotFoundError):
        await users_service.get_user_by_email(email=FakeUserConfig.EMAIL)


@pytest.mark.anyio
async def test_users_service_check_user_existence_success_by_id() -> None:
    users_repository: UsersRepository = await create_fake_users_repository_instance(with_user=True)
    users_statistics_repository: UsersStatisticsRepository = await create_fake_users_statistics_repository_instance(
        with_user=True
    )
    users_unit_of_work: UsersUnitOfWork = FakeUsersUnitOfWork(
        users_repository=users_repository,
        users_statistics_repository=users_statistics_repository,
        users_votes_repository=FakeUsersVotesRepository()
    )
    users_service: UsersService = UsersService(uow=users_unit_of_work)

    assert len(await users_repository.list()) == 1
    assert await users_service.check_user_existence(id=1)


@pytest.mark.anyio
async def test_users_service_check_user_existence_success_by_email() -> None:
    users_repository: UsersRepository = await create_fake_users_repository_instance(with_user=True)
    users_statistics_repository: UsersStatisticsRepository = await create_fake_users_statistics_repository_instance(
        with_user=True
    )
    users_unit_of_work: UsersUnitOfWork = FakeUsersUnitOfWork(
        users_repository=users_repository,
        users_statistics_repository=users_statistics_repository,
        users_votes_repository=FakeUsersVotesRepository()
    )
    users_service: UsersService = UsersService(uow=users_unit_of_work)

    assert len(await users_repository.list()) == 1
    assert await users_service.check_user_existence(email=FakeUserConfig.EMAIL)


@pytest.mark.anyio
async def test_users_service_check_user_existence_success_by_username() -> None:
    users_repository: UsersRepository = await create_fake_users_repository_instance(with_user=True)
    users_statistics_repository: UsersStatisticsRepository = await create_fake_users_statistics_repository_instance(
        with_user=True
    )
    users_unit_of_work: UsersUnitOfWork = FakeUsersUnitOfWork(
        users_repository=users_repository,
        users_statistics_repository=users_statistics_repository,
        users_votes_repository=FakeUsersVotesRepository()
    )
    users_service: UsersService = UsersService(uow=users_unit_of_work)

    assert len(await users_repository.list()) == 1
    assert await users_service.check_user_existence(username=FakeUserConfig.USERNAME)


@pytest.mark.anyio
async def test_users_service_check_user_existence_fail_user_does_not_exist() -> None:
    users_repository: UsersRepository = await create_fake_users_repository_instance()
    users_statistics_repository: UsersStatisticsRepository = await create_fake_users_statistics_repository_instance()
    users_unit_of_work: UsersUnitOfWork = FakeUsersUnitOfWork(
        users_repository=users_repository,
        users_statistics_repository=users_statistics_repository,
        users_votes_repository=FakeUsersVotesRepository()
    )
    users_service: UsersService = UsersService(uow=users_unit_of_work)

    assert len(await users_repository.list()) == 0
    assert not await users_service.check_user_existence(username=FakeUserConfig.USERNAME)


@pytest.mark.anyio
async def test_users_service_check_user_existence_fail_no_attributes_provided() -> None:
    users_repository: UsersRepository = await create_fake_users_repository_instance()
    users_statistics_repository: UsersStatisticsRepository = await create_fake_users_statistics_repository_instance()
    users_unit_of_work: UsersUnitOfWork = FakeUsersUnitOfWork(
        users_repository=users_repository,
        users_statistics_repository=users_statistics_repository,
        users_votes_repository=FakeUsersVotesRepository()
    )
    users_service: UsersService = UsersService(uow=users_unit_of_work)
    with pytest.raises(ValueError) as exc_info:
        await users_service.check_user_existence()

    assert str(exc_info.value) == ErrorDetails.USER_ATTRIBUTE_REQUIRED


@pytest.mark.anyio
async def test_users_service_get_user_by_username_success() -> None:
    users_repository: UsersRepository = await create_fake_users_repository_instance(with_user=True)
    users_statistics_repository: UsersStatisticsRepository = await create_fake_users_statistics_repository_instance(
        with_user=True
    )
    users_unit_of_work: UsersUnitOfWork = FakeUsersUnitOfWork(
        users_repository=users_repository,
        users_statistics_repository=users_statistics_repository,
        users_votes_repository=FakeUsersVotesRepository()
    )
    users_service: UsersService = UsersService(uow=users_unit_of_work)

    assert len(await users_repository.list()) == 1
    found_user: UserModel = await users_service.get_user_by_username(username=FakeUserConfig.USERNAME)
    assert found_user.email == FakeUserConfig.EMAIL
    assert found_user.username == FakeUserConfig.USERNAME
    assert found_user.id == 1


@pytest.mark.anyio
async def test_users_service_get_user_by_username_fail() -> None:
    users_repository: UsersRepository = await create_fake_users_repository_instance()
    users_statistics_repository: UsersStatisticsRepository = await create_fake_users_statistics_repository_instance()
    users_unit_of_work: UsersUnitOfWork = FakeUsersUnitOfWork(
        users_repository=users_repository,
        users_statistics_repository=users_statistics_repository,
        users_votes_repository=FakeUsersVotesRepository()
    )
    users_service: UsersService = UsersService(uow=users_unit_of_work)

    assert len(await users_repository.list()) == 0
    with pytest.raises(UserNotFoundError):
        await users_service.get_user_by_username(username=FakeUserConfig.USERNAME)


@pytest.mark.anyio
async def test_users_service_get_all_users_with_existing_user() -> None:
    users_repository: UsersRepository = await create_fake_users_repository_instance(with_user=True)
    users_statistics_repository: UsersStatisticsRepository = await create_fake_users_statistics_repository_instance(
        with_user=True
    )
    users_unit_of_work: UsersUnitOfWork = FakeUsersUnitOfWork(
        users_repository=users_repository,
        users_statistics_repository=users_statistics_repository,
        users_votes_repository=FakeUsersVotesRepository()
    )
    users_service: UsersService = UsersService(uow=users_unit_of_work)

    users: List[UserModel] = await users_service.get_all_users()
    assert len(users) == 1


@pytest.mark.anyio
async def test_users_service_get_all_users_without_existing_users() -> None:
    users_repository: UsersRepository = await create_fake_users_repository_instance()
    users_statistics_repository: UsersStatisticsRepository = await create_fake_users_statistics_repository_instance()
    users_unit_of_work: UsersUnitOfWork = FakeUsersUnitOfWork(
        users_repository=users_repository,
        users_statistics_repository=users_statistics_repository,
        users_votes_repository=FakeUsersVotesRepository()
    )
    users_service: UsersService = UsersService(uow=users_unit_of_work)

    users: List[UserModel] = await users_service.get_all_users()
    assert len(users) == 0


@pytest.mark.anyio
async def test_get_user_statistics_by_user_id_success() -> None:
    users_repository: UsersRepository = await create_fake_users_repository_instance(with_user=True)
    users_statistics_repository: UsersStatisticsRepository = await create_fake_users_statistics_repository_instance(
        with_user=True
    )
    users_unit_of_work: UsersUnitOfWork = FakeUsersUnitOfWork(
        users_repository=users_repository,
        users_statistics_repository=users_statistics_repository,
        users_votes_repository=FakeUsersVotesRepository()
    )
    users_service: UsersService = UsersService(uow=users_unit_of_work)

    user_statistics: UserStatisticsModel = await users_service.get_user_statistics_by_user_id(user_id=1)
    assert user_statistics.likes == 0
    assert user_statistics.dislikes == 0


@pytest.mark.anyio
async def test_get_user_statistics_by_user_id_fail_user_statistics_not_found() -> None:
    users_repository: UsersRepository = await create_fake_users_repository_instance()
    users_statistics_repository: UsersStatisticsRepository = await create_fake_users_statistics_repository_instance()
    users_unit_of_work: UsersUnitOfWork = FakeUsersUnitOfWork(
        users_repository=users_repository,
        users_statistics_repository=users_statistics_repository,
        users_votes_repository=FakeUsersVotesRepository()
    )
    users_service: UsersService = UsersService(uow=users_unit_of_work)

    with pytest.raises(UserStatisticsNotFoundError):
        await users_service.get_user_statistics_by_user_id(user_id=1)


@pytest.mark.anyio
async def test_like_user_success() -> None:
    users_repository: UsersRepository = await create_fake_users_repository_instance(with_user=True)
    users_statistics_repository: UsersStatisticsRepository = await create_fake_users_statistics_repository_instance(
        with_user=True
    )
    users_unit_of_work: UsersUnitOfWork = FakeUsersUnitOfWork(
        users_repository=users_repository,
        users_statistics_repository=users_statistics_repository,
        users_votes_repository=FakeUsersVotesRepository()
    )
    users_service: UsersService = UsersService(uow=users_unit_of_work)

    user_statistics: UserStatisticsModel = await users_service.like_user(voting_user_id=1, voted_for_user_id=1)
    assert user_statistics.likes == 1
    assert user_statistics.dislikes == 0


@pytest.mark.anyio
async def test_like_user_fail_user_statistics_not_found() -> None:
    users_repository: UsersRepository = await create_fake_users_repository_instance()
    users_statistics_repository: UsersStatisticsRepository = await create_fake_users_statistics_repository_instance()
    users_unit_of_work: UsersUnitOfWork = FakeUsersUnitOfWork(
        users_repository=users_repository,
        users_statistics_repository=users_statistics_repository,
        users_votes_repository=FakeUsersVotesRepository()
    )
    users_service: UsersService = UsersService(uow=users_unit_of_work)

    with pytest.raises(UserStatisticsNotFoundError):
        await users_service.like_user(voting_user_id=1, voted_for_user_id=1)


@pytest.mark.anyio
async def test_dislike_user_success() -> None:
    users_repository: UsersRepository = await create_fake_users_repository_instance(with_user=True)
    users_statistics_repository: UsersStatisticsRepository = await create_fake_users_statistics_repository_instance(
        with_user=True
    )
    users_unit_of_work: UsersUnitOfWork = FakeUsersUnitOfWork(
        users_repository=users_repository,
        users_statistics_repository=users_statistics_repository,
        users_votes_repository=FakeUsersVotesRepository()
    )
    users_service: UsersService = UsersService(uow=users_unit_of_work)

    user_statistics: UserStatisticsModel = await users_service.dislike_user(voting_user_id=1, voted_for_user_id=1)
    assert user_statistics.likes == 0
    assert user_statistics.dislikes == 1


@pytest.mark.anyio
async def test_dislike_user_fail_user_statistics_not_found() -> None:
    users_repository: UsersRepository = await create_fake_users_repository_instance()
    users_statistics_repository: UsersStatisticsRepository = await create_fake_users_statistics_repository_instance()
    users_unit_of_work: UsersUnitOfWork = FakeUsersUnitOfWork(
        users_repository=users_repository,
        users_statistics_repository=users_statistics_repository,
        users_votes_repository=FakeUsersVotesRepository()
    )
    users_service: UsersService = UsersService(uow=users_unit_of_work)

    with pytest.raises(UserStatisticsNotFoundError):
        await users_service.dislike_user(voting_user_id=1, voted_for_user_id=1)


@pytest.mark.anyio
async def test_check_if_user_already_voted_success() -> None:
    users_repository: UsersRepository = await create_fake_users_repository_instance(with_user=True)
    users_statistics_repository: UsersStatisticsRepository = await create_fake_users_statistics_repository_instance(
        with_user=True
    )
    users_unit_of_work: UsersUnitOfWork = FakeUsersUnitOfWork(
        users_repository=users_repository,
        users_statistics_repository=users_statistics_repository,
        users_votes_repository=FakeUsersVotesRepository(
            users_votes={
                1: UserVoteModel(
                    voting_user_id=1,
                    voted_for_user_id=1
                )
            }
        )
    )
    users_service: UsersService = UsersService(uow=users_unit_of_work)

    assert await users_service.check_if_user_already_voted(voting_user_id=1, voted_for_user_id=1)


@pytest.mark.anyio
async def test_check_if_user_already_voted_fail() -> None:
    users_repository: UsersRepository = await create_fake_users_repository_instance()
    users_statistics_repository: UsersStatisticsRepository = await create_fake_users_statistics_repository_instance()
    users_unit_of_work: UsersUnitOfWork = FakeUsersUnitOfWork(
        users_repository=users_repository,
        users_statistics_repository=users_statistics_repository,
        users_votes_repository=FakeUsersVotesRepository()
    )
    users_service: UsersService = UsersService(uow=users_unit_of_work)

    assert not await users_service.check_if_user_already_voted(voting_user_id=1, voted_for_user_id=1)
