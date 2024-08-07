from fastapi import Depends
from typing import List

from src.core.bootstrap import Bootstrap
from src.core.messagebus import MessageBus
from src.users.domain.models import UserModel, UserStatisticsModel
from src.security.models import JWTDataModel
from src.users.entrypoints.schemas import LoginUserScheme, RegisterUserScheme
from src.users.service_layer.handlers import EVENTS_HANDLERS_FOR_INJECTION, COMMANDS_HANDLERS_FOR_INJECTION
from src.users.utils import oauth2_scheme
from src.security.utils import parse_jwt_token
from src.users.service_layer.units_of_work import SQLAlchemyUsersUnitOfWork
from src.users.entrypoints.views import UsersViews
from src.users.domain.commands import (
    RegisterUserCommand,
    VoteForUserCommand,
    VerifyUserCredentialsCommand
)


"""
Can not use Bootstrap object in dependencies, so its defined in each dependency body.
"""


async def register_user(user_data: RegisterUserScheme) -> UserModel:
    bootstrap: Bootstrap = Bootstrap(
        uow=SQLAlchemyUsersUnitOfWork(),
        events_handlers_for_injection=EVENTS_HANDLERS_FOR_INJECTION,
        commands_handlers_for_injection=COMMANDS_HANDLERS_FOR_INJECTION
    )

    messagebus: MessageBus = await bootstrap.get_messagebus()
    await messagebus.handle(
        RegisterUserCommand(
            **user_data.model_dump()
        )
    )

    return messagebus.command_result


async def verify_user_credentials(user_data: LoginUserScheme) -> UserModel:
    bootstrap: Bootstrap = Bootstrap(
        uow=SQLAlchemyUsersUnitOfWork(),
        events_handlers_for_injection=EVENTS_HANDLERS_FOR_INJECTION,
        commands_handlers_for_injection=COMMANDS_HANDLERS_FOR_INJECTION
    )

    messagebus: MessageBus = await bootstrap.get_messagebus()
    await messagebus.handle(
        VerifyUserCredentialsCommand(
            **user_data.model_dump()
        )
    )

    return messagebus.command_result


async def get_my_account(token: str = Depends(oauth2_scheme)) -> UserModel:
    jwt_data: JWTDataModel = await parse_jwt_token(token=token)
    users_views: UsersViews = UsersViews(uow=SQLAlchemyUsersUnitOfWork())
    return await users_views.get_user_account(user_id=jwt_data.user_id)


async def get_my_statistics(token: str = Depends(oauth2_scheme)) -> UserStatisticsModel:
    jwt_data: JWTDataModel = await parse_jwt_token(token=token)
    users_views: UsersViews = UsersViews(uow=SQLAlchemyUsersUnitOfWork())
    return await users_views.get_user_statistics(user_id=jwt_data.user_id)


async def like_user(user_id: int, token: str = Depends(oauth2_scheme)) -> UserStatisticsModel:
    jwt_data: JWTDataModel = await parse_jwt_token(token=token)
    bootstrap: Bootstrap = Bootstrap(
        uow=SQLAlchemyUsersUnitOfWork(),
        events_handlers_for_injection=EVENTS_HANDLERS_FOR_INJECTION,
        commands_handlers_for_injection=COMMANDS_HANDLERS_FOR_INJECTION
    )

    messagebus: MessageBus = await bootstrap.get_messagebus()
    await messagebus.handle(
        VoteForUserCommand(
            voted_for_user_id=user_id,
            voting_user_id=jwt_data.user_id,
            liked=True,
            disliked=False
        )
    )

    return messagebus.command_result


async def dislike_user(user_id: int, token: str = Depends(oauth2_scheme)) -> UserStatisticsModel:
    jwt_data: JWTDataModel = await parse_jwt_token(token=token)
    bootstrap: Bootstrap = Bootstrap(
        uow=SQLAlchemyUsersUnitOfWork(),
        events_handlers_for_injection=EVENTS_HANDLERS_FOR_INJECTION,
        commands_handlers_for_injection=COMMANDS_HANDLERS_FOR_INJECTION
    )

    messagebus: MessageBus = await bootstrap.get_messagebus()
    await messagebus.handle(
        VoteForUserCommand(
            voted_for_user_id=user_id,
            voting_user_id=jwt_data.user_id,
            liked=False,
            disliked=True
        )
    )

    return messagebus.command_result


async def get_all_users() -> List[UserModel]:
    users_views: UsersViews = UsersViews(uow=SQLAlchemyUsersUnitOfWork())
    return await users_views.get_all_users()
