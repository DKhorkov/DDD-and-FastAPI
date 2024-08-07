from src.users.domain.events import UserVotedEvent
from src.users.interfaces.handlers import UsersCommandHandler
from src.users.domain.commands import (
    VerifyUserCredentialsCommand,
    RegisterUserCommand,
    VoteForUserCommand
)
from src.users.domain.models import UserModel, UserStatisticsModel
from src.users.exceptions import (
    InvalidPasswordError,
    UserAlreadyExistsError,
    UserNotFoundError,
    UserAlreadyVotedError,
    UserCanNotVoteForHimSelf
)
from src.users.service_layer.service import UsersService
from src.users.utils import hash_password, verify_password


class RegisterUserCommandHandler(UsersCommandHandler):

    async def __call__(self, command: RegisterUserCommand) -> UserModel:
        """
        Registers a new user, if user with provided credentials doesn't exist, and creates event signaling that
        operation was successfully executed.
        """

        users_service: UsersService = UsersService(uow=self._uow)
        if await users_service.check_user_existence(email=command.email, username=command.username):
            raise UserAlreadyExistsError

        user: UserModel = UserModel(**await command.to_dict())
        user.password = await hash_password(user.password)

        user = await users_service.register_user(user=user)
        return user


class VerifyUserCredentialsCommandHandler(UsersCommandHandler):

    async def __call__(self, command: VerifyUserCredentialsCommand) -> UserModel:
        """
        Checks, if provided by user credentials are valid.
        """

        users_service: UsersService = UsersService(uow=self._uow)

        user: UserModel
        if await users_service.check_user_existence(email=command.username):
            user = await users_service.get_user_by_email(email=command.username)
        elif await users_service.check_user_existence(username=command.username):
            user = await users_service.get_user_by_username(username=command.username)
        else:
            raise UserNotFoundError

        if not await verify_password(plain_password=command.password, hashed_password=user.password):
            raise InvalidPasswordError

        return user


class VoteForUserCommandHandler(UsersCommandHandler):

    async def __call__(self, command: VoteForUserCommand) -> UserStatisticsModel:
        """
        1) Checks, if a vote is appropriate.
        2) Likes or dislikes user, depends on from command data.
        3) Creates event, signaling that user has voted.
        """

        async with self._uow as uow:
            if command.voting_user_id == command.voted_for_user_id:
                raise UserCanNotVoteForHimSelf

            users_service: UsersService = UsersService(uow=uow)
            if await users_service.check_if_user_already_voted(
                    voting_user_id=command.voting_user_id,
                    voted_for_user_id=command.voted_for_user_id
            ):
                raise UserAlreadyVotedError

            user_statistics: UserStatisticsModel
            if command.liked:
                user_statistics = await users_service.like_user(
                    voting_user_id=command.voting_user_id,
                    voted_for_user_id=command.voted_for_user_id
                )
            else:
                user_statistics = await users_service.dislike_user(
                    voting_user_id=command.voting_user_id,
                    voted_for_user_id=command.voted_for_user_id
                )

            voted_for_user: UserModel = await users_service.get_user_by_id(id=command.voted_for_user_id)
            voting_user: UserModel = await users_service.get_user_by_id(id=command.voting_user_id)
            await uow.add_event(
                UserVotedEvent(
                    liked=command.liked,
                    disliked=command.disliked,
                    voted_for_user_email=voted_for_user.email,
                    voted_for_user_username=voted_for_user.username,
                    voting_user_username=voting_user.username,
                    voting_user_email=voting_user.email,
                )
            )

            return user_statistics
