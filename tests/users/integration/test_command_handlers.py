import pytest
from typing import List

from src.core.interfaces import AbstractEvent
from src.users.domain.commands import (
    RegisterUserCommand,
    VerifyUserCredentialsCommand
)
from src.users.domain.events import UserRegisteredEvent
from src.users.domain.models import UserModel
from src.users.exceptions import (
    UserAlreadyExistsError,
    EmailIsNotVerifiedError,
    InvalidPasswordError,
    UserNotFoundError
)
from src.users.interfaces import UsersUnitOfWork, UsersRepository
from src.users.service_layer.handlers.command_handlers import (
    RegisterUserCommandHandler,
    VerifyUserCredentialsCommandHandler
)
from tests.config import FakeUserConfig
from tests.users.fake_objects import FakeUsersUnitOfWork, FakeUsersRepository
from tests.users.utils import create_fake_users_repository_instance


@pytest.mark.anyio
async def test_register_user_command_handler_success() -> None:
    users_repository: UsersRepository = await create_fake_users_repository_instance()
    users_unit_of_work: UsersUnitOfWork = FakeUsersUnitOfWork(users_repository=users_repository)
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
    assert not user.password

    events: List[AbstractEvent] = list(users_unit_of_work.get_events())
    assert len(events) == 1
    assert isinstance(events[0], UserRegisteredEvent)


@pytest.mark.anyio
async def test_register_user_command_handler_fail_user_already_exists() -> None:
    users_repository: UsersRepository = await create_fake_users_repository_instance(with_user=True)
    users_unit_of_work: UsersUnitOfWork = FakeUsersUnitOfWork(users_repository=users_repository)
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
    users_unit_of_work: UsersUnitOfWork = FakeUsersUnitOfWork(users_repository=users_repository)
    handler: VerifyUserCredentialsCommandHandler = VerifyUserCredentialsCommandHandler(uow=users_unit_of_work)
    user: UserModel = await handler(
        command=VerifyUserCredentialsCommand(
            username=FakeUserConfig.EMAIL,
            password=FakeUserConfig.PASSWORD
        )
    )

    assert user.email == FakeUserConfig.EMAIL
    assert user.username == FakeUserConfig.USERNAME
    assert not user.password


@pytest.mark.anyio
async def test_verify_user_credentials_command_handler_via_username_success() -> None:
    users_repository: UsersRepository = await create_fake_users_repository_instance(with_user=True)
    users_unit_of_work: UsersUnitOfWork = FakeUsersUnitOfWork(users_repository=users_repository)
    handler: VerifyUserCredentialsCommandHandler = VerifyUserCredentialsCommandHandler(uow=users_unit_of_work)
    user: UserModel = await handler(
        command=VerifyUserCredentialsCommand(
            username=FakeUserConfig.USERNAME,
            password=FakeUserConfig.PASSWORD
        )
    )

    assert user.email == FakeUserConfig.EMAIL
    assert user.username == FakeUserConfig.USERNAME
    assert not user.password


@pytest.mark.anyio
async def test_verify_user_credentials_command_handler_fail_user_not_found() -> None:
    users_repository: UsersRepository = await create_fake_users_repository_instance()
    users_unit_of_work: UsersUnitOfWork = FakeUsersUnitOfWork(users_repository=users_repository)
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
    users_unit_of_work: UsersUnitOfWork = FakeUsersUnitOfWork(users_repository=users_repository)
    handler: VerifyUserCredentialsCommandHandler = VerifyUserCredentialsCommandHandler(uow=users_unit_of_work)
    with pytest.raises(InvalidPasswordError):
        await handler(
            command=VerifyUserCredentialsCommand(
                username=FakeUserConfig.USERNAME,
                password='some trash password'
            )
        )


@pytest.mark.anyio
async def test_verify_user_credentials_command_handler_fail_email_is_not_verified() -> None:
    user_id: int = 1
    user_data: FakeUserConfig = FakeUserConfig()
    user_data.EMAIL_VERIFIED = False
    user: UserModel = UserModel(**user_data.to_dict(to_lower=True), id=user_id)
    users_repository = FakeUsersRepository(users={user_id: user})
    users_unit_of_work: UsersUnitOfWork = FakeUsersUnitOfWork(users_repository=users_repository)
    handler: VerifyUserCredentialsCommandHandler = VerifyUserCredentialsCommandHandler(uow=users_unit_of_work)
    with pytest.raises(EmailIsNotVerifiedError):
        await handler(
            command=VerifyUserCredentialsCommand(
                username=FakeUserConfig.USERNAME,
                password=FakeUserConfig.PASSWORD
            )
        )
