from typing import Optional, List, Sequence
from sqlalchemy.ext.asyncio import async_sessionmaker
from sqlalchemy import select

from src.users.constants import ErrorDetails
from src.users.exceptions import UserNotFoundError
from src.users.models import UserModel
from src.core.database.connection import session_factory as default_session_factory


class UsersService:
    """
    Service layer core according to DDD, which using a unit of work, will perform operations on the domain model.
    """

    def __init__(self, session_factory: async_sessionmaker = default_session_factory) -> None:
        self._session_factory: async_sessionmaker = session_factory

    async def register_user(self, user: UserModel) -> UserModel:
        async with self._session_factory() as session:
            session.add(user)
            await session.commit()
            return await self.get_user_by_email(email=user.email)

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
