import pytest
from typing import List

from src.core.interfaces import AbstractEvent
from src.users.domain.commands import (
    RegisterUserCommand,
    VerifyUserCredentialsCommand,
    VoteForUserCommand
)
from src.users.domain.events import UserVotedEvent
from src.users.domain.models import UserModel, UserVoteModel, UserStatisticsModel
from src.users.exceptions import (
    InvalidPasswordError,
    UserAlreadyExistsError,
    UserNotFoundError,
    UserAlreadyVotedError,
    UserCanNotVoteForHimSelf
)
from src.users.interfaces import UsersUnitOfWork, UsersRepository, UsersStatisticsRepository
from src.users.service_layer.handlers.command_handlers import (
    RegisterUserCommandHandler,
    VerifyUserCredentialsCommandHandler,
    VoteForUserCommandHandler
)
from tests.config import FakeUserConfig
from tests.users.fake_objects import FakeUsersUnitOfWork, FakeUsersVotesRepository
from tests.users.utils import create_fake_users_repository_instance, create_fake_users_statistics_repository_instance


@pytest.mark.anyio
async def test_register_user_command_handler_success() -> None:
    users_repository: UsersRepository = await create_fake_users_repository_instance()
    users_statistics_repository: UsersStatisticsRepository = await create_fake_users_statistics_repository_instance()
    users_unit_of_work: UsersUnitOfWork = FakeUsersUnitOfWork(
        users_repository=users_repository,
        users_statistics_repository=users_statistics_repository,
        users_votes_repository=FakeUsersVotesRepository()
    )

    handler: RegisterUserCommandHandler = RegisterUserCommandHandler(uow=users_unit_of_work)
    user: UserModel = await handler(
        command=RegisterUserCommand(
            username=FakeUserConfig.USERNAME,
            email=FakeUserConfig.EMAIL,
            password=FakeUserConfig.PASSWORD
        )
    )

    assert user.email == FakeUserConfig.EMAIL
    assert user.username == FakeUserConfig.USERNAME


@pytest.mark.anyio
async def test_register_user_command_handler_fail_user_already_exists() -> None:
    users_repository: UsersRepository = await create_fake_users_repository_instance(with_user=True)
    users_statistics_repository: UsersStatisticsRepository = await create_fake_users_statistics_repository_instance(
        with_user=True
    )

    users_unit_of_work: UsersUnitOfWork = FakeUsersUnitOfWork(
        users_repository=users_repository,
        users_statistics_repository=users_statistics_repository,
        users_votes_repository=FakeUsersVotesRepository()
    )

    handler: RegisterUserCommandHandler = RegisterUserCommandHandler(uow=users_unit_of_work)
    with pytest.raises(UserAlreadyExistsError):
        await handler(
            command=RegisterUserCommand(
                username=FakeUserConfig.USERNAME,
                email=FakeUserConfig.EMAIL,
                password=FakeUserConfig.PASSWORD
            )
        )


@pytest.mark.anyio
async def test_verify_user_credentials_command_handler_via_email_success() -> None:
    users_repository: UsersRepository = await create_fake_users_repository_instance(with_user=True)
    users_statistics_repository: UsersStatisticsRepository = await create_fake_users_statistics_repository_instance(
        with_user=True
    )

    users_unit_of_work: UsersUnitOfWork = FakeUsersUnitOfWork(
        users_repository=users_repository,
        users_statistics_repository=users_statistics_repository,
        users_votes_repository=FakeUsersVotesRepository()
    )

    handler: VerifyUserCredentialsCommandHandler = VerifyUserCredentialsCommandHandler(uow=users_unit_of_work)
    user: UserModel = await handler(
        command=VerifyUserCredentialsCommand(
            username=FakeUserConfig.EMAIL,
            password=FakeUserConfig.PASSWORD
        )
    )

    assert user.email == FakeUserConfig.EMAIL
    assert user.username == FakeUserConfig.USERNAME


@pytest.mark.anyio
async def test_verify_user_credentials_command_handler_via_username_success() -> None:
    users_repository: UsersRepository = await create_fake_users_repository_instance(with_user=True)
    users_statistics_repository: UsersStatisticsRepository = await create_fake_users_statistics_repository_instance(
        with_user=True
    )

    users_unit_of_work: UsersUnitOfWork = FakeUsersUnitOfWork(
        users_repository=users_repository,
        users_statistics_repository=users_statistics_repository,
        users_votes_repository=FakeUsersVotesRepository()
    )

    handler: VerifyUserCredentialsCommandHandler = VerifyUserCredentialsCommandHandler(uow=users_unit_of_work)
    user: UserModel = await handler(
        command=VerifyUserCredentialsCommand(
            username=FakeUserConfig.USERNAME,
            password=FakeUserConfig.PASSWORD
        )
    )

    assert user.email == FakeUserConfig.EMAIL
    assert user.username == FakeUserConfig.USERNAME


@pytest.mark.anyio
async def test_verify_user_credentials_command_handler_fail_user_not_found() -> None:
    users_repository: UsersRepository = await create_fake_users_repository_instance()
    users_statistics_repository: UsersStatisticsRepository = await create_fake_users_statistics_repository_instance()
    users_unit_of_work: UsersUnitOfWork = FakeUsersUnitOfWork(
        users_repository=users_repository,
        users_statistics_repository=users_statistics_repository,
        users_votes_repository=FakeUsersVotesRepository()
    )

    handler: VerifyUserCredentialsCommandHandler = VerifyUserCredentialsCommandHandler(uow=users_unit_of_work)
    with pytest.raises(UserNotFoundError):
        await handler(
            command=VerifyUserCredentialsCommand(
                username=FakeUserConfig.USERNAME,
                password=FakeUserConfig.PASSWORD
            )
        )


@pytest.mark.anyio
async def test_verify_user_credentials_command_handler_fail_invalid_password() -> None:
    users_repository: UsersRepository = await create_fake_users_repository_instance(with_user=True)
    users_statistics_repository: UsersStatisticsRepository = await create_fake_users_statistics_repository_instance(
        with_user=True
    )

    users_unit_of_work: UsersUnitOfWork = FakeUsersUnitOfWork(
        users_repository=users_repository,
        users_statistics_repository=users_statistics_repository,
        users_votes_repository=FakeUsersVotesRepository()
    )

    handler: VerifyUserCredentialsCommandHandler = VerifyUserCredentialsCommandHandler(uow=users_unit_of_work)
    with pytest.raises(InvalidPasswordError):
        await handler(
            command=VerifyUserCredentialsCommand(
                username=FakeUserConfig.USERNAME,
                password='some trash password'
            )
        )


@pytest.mark.anyio
async def test_vote_for_user_command_handler_fail_user_can_not_vote_for_himself() -> None:
    users_repository: UsersRepository = await create_fake_users_repository_instance(with_user=True)
    users_statistics_repository: UsersStatisticsRepository = await create_fake_users_statistics_repository_instance(
        with_user=True
    )

    users_unit_of_work: UsersUnitOfWork = FakeUsersUnitOfWork(
        users_repository=users_repository,
        users_statistics_repository=users_statistics_repository,
        users_votes_repository=FakeUsersVotesRepository()
    )

    handler: VoteForUserCommandHandler = VoteForUserCommandHandler(uow=users_unit_of_work)
    with pytest.raises(UserCanNotVoteForHimSelf):
        await handler(
            command=VoteForUserCommand(
                voted_for_user_id=1,
                voting_user_id=1,
                liked=True,
                disliked=False
            )
        )


@pytest.mark.anyio
async def test_vote_for_user_command_handler_fail_user_can_not_vote_twice_for_same_user() -> None:
    users_repository: UsersRepository = await create_fake_users_repository_instance(with_user=True)
    await users_repository.add(
        UserModel(
            id=2,
            email='test_email@gmail.com',
            password='<PASSWORD>',
            username='test_username'
        )
    )

    users_statistics_repository: UsersStatisticsRepository = await create_fake_users_statistics_repository_instance(
        with_user=True
    )
    await users_statistics_repository.add(
        UserStatisticsModel(
            id=2,
            user_id=2
        )
    )

    users_unit_of_work: UsersUnitOfWork = FakeUsersUnitOfWork(
        users_repository=users_repository,
        users_statistics_repository=users_statistics_repository,
        users_votes_repository=FakeUsersVotesRepository(
            users_votes={
                1: UserVoteModel(
                    voting_user_id=1,
                    voted_for_user_id=2
                )
            }
        )
    )

    handler: VoteForUserCommandHandler = VoteForUserCommandHandler(uow=users_unit_of_work)
    with pytest.raises(UserAlreadyVotedError):
        await handler(
            command=VoteForUserCommand(
                voted_for_user_id=2,
                voting_user_id=1,
                liked=True,
                disliked=False
            )
        )


@pytest.mark.anyio
async def test_vote_for_user_command_handler_success() -> None:
    users_repository: UsersRepository = await create_fake_users_repository_instance(with_user=True)
    await users_repository.add(
        UserModel(
            id=2,
            email='test_email@gmail.com',
            password='<PASSWORD>',
            username='test_username'
        )
    )

    users_statistics_repository: UsersStatisticsRepository = await create_fake_users_statistics_repository_instance(
        with_user=True
    )
    await users_statistics_repository.add(
        UserStatisticsModel(
            id=2,
            user_id=2
        )
    )

    users_unit_of_work: UsersUnitOfWork = FakeUsersUnitOfWork(
        users_repository=users_repository,
        users_statistics_repository=users_statistics_repository,
        users_votes_repository=FakeUsersVotesRepository()
    )

    handler: VoteForUserCommandHandler = VoteForUserCommandHandler(uow=users_unit_of_work)
    await handler(
        command=VoteForUserCommand(
            voted_for_user_id=2,
            voting_user_id=1,
            liked=True,
            disliked=False
        )
    )

    events: List[AbstractEvent] = list(users_unit_of_work.get_events())
    assert len(events) == 1
    assert isinstance(events[0], UserVotedEvent)
