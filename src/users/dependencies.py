from fastapi import Depends
from typing import List

from src.users.exceptions import (
    UserNotFoundError,
    InvalidPasswordError,
    UserAlreadyExistsError,
    UserAlreadyVotedError,
    UserCanNotVoteForHimSelf
)
from src.users.models import UserModel, UserStatisticsModel
from src.security.models import JWTDataModel
from src.users.schemas import LoginUserScheme, RegisterUserScheme
from src.users.utils import oauth2_scheme, verify_password, hash_password
from src.security.utils import parse_jwt_token
from src.users.service import UsersService


async def register_user(user_data: RegisterUserScheme) -> UserModel:
    users_service: UsersService = UsersService()
    if await users_service.check_user_existence(email=user_data.email, username=user_data.username):
        raise UserAlreadyExistsError

    user: UserModel = UserModel(**user_data.model_dump())
    user.password = await hash_password(user.password)
    return await users_service.register_user(user=user)


async def verify_user_credentials(user_data: LoginUserScheme) -> UserModel:
    users_service: UsersService = UsersService()
    user: UserModel
    if await users_service.check_user_existence(email=user_data.username):
        user = await users_service.get_user_by_email(email=user_data.username)
    elif await users_service.check_user_existence(username=user_data.username):
        user = await users_service.get_user_by_username(username=user_data.username)
    else:
        raise UserNotFoundError

    if not await verify_password(plain_password=user_data.password, hashed_password=user.password):
        raise InvalidPasswordError

    return user


async def authenticate_user(token: str = Depends(oauth2_scheme)) -> UserModel:
    """
    Authenticates user according to provided JWT token, if token is valid and hadn't expired.
    """

    jwt_data: JWTDataModel = await parse_jwt_token(token=token)
    users_service: UsersService = UsersService()
    user: UserModel = await users_service.get_user_by_id(id=jwt_data.user_id)
    return user


async def get_my_account(user: UserModel = Depends(authenticate_user)) -> UserModel:
    return user


async def get_my_statistics(user: UserModel = Depends(authenticate_user)) -> UserStatisticsModel:
    users_service: UsersService = UsersService()
    user_statistics: UserStatisticsModel = await users_service.get_user_statistics_by_user_id(user_id=user.id)
    return user_statistics


async def like_user(user_id: int, user: UserModel = Depends(authenticate_user)) -> UserStatisticsModel:
    if user.id == user_id:
        raise UserCanNotVoteForHimSelf

    users_service: UsersService = UsersService()
    if await users_service.check_if_user_already_voted(voting_user_id=user.id, voted_for_user_id=user_id):
        raise UserAlreadyVotedError

    user_statistics: UserStatisticsModel = await users_service.like_user(
        voting_user_id=user.id,
        voted_for_user_id=user_id
    )

    return user_statistics


async def dislike_user(user_id: int, user: UserModel = Depends(authenticate_user)) -> UserStatisticsModel:
    if user.id == user_id:
        raise UserCanNotVoteForHimSelf

    users_service: UsersService = UsersService()
    if await users_service.check_if_user_already_voted(voting_user_id=user.id, voted_for_user_id=user_id):
        raise UserAlreadyVotedError

    user_statistics: UserStatisticsModel = await users_service.dislike_user(
        voting_user_id=user.id,
        voted_for_user_id=user_id
    )

    return user_statistics


async def get_all_users() -> List[UserModel]:
    users_service: UsersService = UsersService()
    users: List[UserModel] = await users_service.get_all_users()
    return users
