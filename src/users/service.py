from typing import Optional, List, Sequence
from sqlalchemy.ext.asyncio import async_sessionmaker
from sqlalchemy import select, update, insert

from src.users.constants import ErrorDetails
from src.users.exceptions import UserNotFoundError, UserStatisticsNotFoundError
from src.users.models import UserModel, UserStatisticsModel, UserVoteModel
from src.core.database.connection import session_factory as default_session_factory


class UsersService:

    def __init__(self, session_factory: async_sessionmaker = default_session_factory) -> None:
        self._session_factory: async_sessionmaker = session_factory

    async def register_user(self, user: UserModel) -> UserModel:
        async with self._session_factory() as session:
            session.add(user)
            await session.flush()
            session.add(UserStatisticsModel(user_id=user.id))
            await session.commit()
            return user

    async def check_user_existence(
            self,
            id: Optional[int] = None,
            email: Optional[str] = None,
            username: Optional[str] = None
    ) -> bool:

        if not (id or email or username):
            raise ValueError(ErrorDetails.USER_ATTRIBUTE_REQUIRED)

        async with self._session_factory() as session:
            user: Optional[UserModel]  # declaring here for mypy passing
            if id:
                user = (await session.scalars(select(UserModel).filter_by(id=id))).one_or_none()
                if user:
                    return True

            if email:
                user = (await session.scalars(select(UserModel).filter_by(email=email))).one_or_none()
                if user:
                    return True

            if username:
                user = (await session.scalars(select(UserModel).filter_by(username=username))).one_or_none()
                if user:
                    return True

        return False

    async def get_user_by_email(self, email: str) -> UserModel:
        async with self._session_factory() as session:
            user: Optional[UserModel] = (await session.scalars(select(UserModel).filter_by(email=email))).one_or_none()
            if not user:
                raise UserNotFoundError

            return user

    async def get_user_by_username(self, username: str) -> UserModel:
        async with self._session_factory() as session:
            user: Optional[UserModel] = (
                await session.scalars(
                    select(
                        UserModel
                    ).filter_by(
                        username=username
                    )
                )
            ).one_or_none()
            if not user:
                raise UserNotFoundError

            return user

    async def get_user_by_id(self, id: int) -> UserModel:
        async with self._session_factory() as session:
            user: Optional[UserModel] = (await session.scalars(select(UserModel).filter_by(id=id))).one_or_none()
            if not user:
                raise UserNotFoundError

            return user

    async def get_all_users(self) -> List[UserModel]:
        async with self._session_factory() as session:
            users: Sequence[UserModel] = (await session.scalars(select(UserModel))).all()
            assert isinstance(users, list)
            return users

    async def get_user_statistics_by_user_id(self, user_id: int) -> UserStatisticsModel:
        async with self._session_factory() as session:
            user_statistics: Optional[UserStatisticsModel] = (
                await session.scalars(
                    select(
                        UserStatisticsModel
                    ).filter_by(
                        user_id=user_id
                    )
                )
            ).one_or_none()
            if not user_statistics:
                raise UserStatisticsNotFoundError

            return user_statistics

    async def like_user(self, voting_user_id: int, voted_for_user_id: int) -> UserStatisticsModel:
        async with self._session_factory() as session:
            user_statistics: Optional[UserStatisticsModel] = (
                await session.scalars(
                    select(
                        UserStatisticsModel
                    ).filter_by(
                        user_id=voted_for_user_id
                    )
                )
            ).one_or_none()
            if not user_statistics:
                raise UserStatisticsNotFoundError

            await session.execute(
                update(
                    UserStatisticsModel
                ).filter_by(
                    id=user_statistics.id
                ).values(
                    likes=user_statistics.likes + 1
                )
            )

            await session.execute(
                insert(
                    UserVoteModel
                ).values(
                    voting_user_id=voting_user_id,
                    voted_for_user_id=voted_for_user_id
                )
            )

            await session.commit()
            return user_statistics

    async def dislike_user(self, voting_user_id: int, voted_for_user_id: int) -> UserStatisticsModel:
        async with self._session_factory() as session:
            user_statistics: Optional[UserStatisticsModel] = (
                await session.scalars(
                    select(
                        UserStatisticsModel
                    ).filter_by(
                        user_id=voted_for_user_id
                    )
                )
            ).one_or_none()
            if not user_statistics:
                raise UserStatisticsNotFoundError

            await session.execute(
                update(
                    UserStatisticsModel
                ).filter_by(
                    id=user_statistics.id
                ).values(
                    dislikes=user_statistics.dislikes + 1
                )
            )

            await session.execute(
                insert(
                    UserVoteModel
                ).values(
                    voting_user_id=voting_user_id,
                    voted_for_user_id=voted_for_user_id
                )
            )

            await session.commit()
            return user_statistics

    async def check_if_user_already_voted(self, voting_user_id: int, voted_for_user_id: int) -> bool:
        async with self._session_factory() as session:
            user_vote: Optional[UserVoteModel] = (
                await session.scalars(
                    select(
                        UserVoteModel
                    ).filter_by(
                        voted_for_user_id=voted_for_user_id,
                        voting_user_id=voting_user_id
                    )
                )
            ).one_or_none()
            if user_vote:
                return True

        return False
