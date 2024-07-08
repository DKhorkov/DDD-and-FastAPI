from typing import List, Optional, Sequence, Any
from sqlalchemy import insert, select, delete, update, Result, RowMapping, Row

from src.users.interfaces.repositories import UsersRepository, UsersStatisticsRepository, UsersVotesRepository
from src.users.domain.models import UserModel, UserStatisticsModel, UserVoteModel
from src.core.database.interfaces.repositories import SQLAlchemyAbstractRepository
from src.core.interfaces import AbstractModel


class SQLAlchemyUsersRepository(SQLAlchemyAbstractRepository, UsersRepository):

    async def get(self, id: int) -> Optional[UserModel]:
        result: Result = await self._session.execute(select(UserModel).filter_by(id=id))
        return result.scalar_one_or_none()

    async def get_by_email(self, email: str) -> Optional[UserModel]:
        result: Result = await self._session.execute(select(UserModel).filter_by(email=email))
        return result.scalar_one_or_none()

    async def get_by_username(self, username: str) -> Optional[UserModel]:
        result: Result = await self._session.execute(select(UserModel).filter_by(username=username))
        return result.scalar_one_or_none()

    async def add(self, model: AbstractModel) -> UserModel:
        result: Result = await self._session.execute(
            insert(UserModel).values(**await model.to_dict(exclude={'id'})).returning(UserModel)
        )

        return result.scalar_one()

    async def update(self, id: int, model: AbstractModel) -> UserModel:
        result: Result = await self._session.execute(
            update(UserModel).filter_by(id=id).values(**await model.to_dict(exclude={'id'})).returning(UserModel)
        )

        return result.scalar_one()

    async def delete(self, id: int) -> None:
        await self._session.execute(delete(UserModel).filter_by(id=id))

    async def list(self) -> List[UserModel]:
        """
        Returning result object instead of converting to new objects by
                    [UserModel(**await r.to_dict()) for r in result.scalars().all()]
        to avoid sqlalchemy.orm.exc.UnmappedInstanceError lately.

        Checking by asserts, that expected return type is equal to fact return type.
        """

        result: Result = await self._session.execute(select(UserModel))
        users: Sequence[Row | RowMapping | Any] = result.scalars().all()

        assert isinstance(users, List)
        for user in users:
            assert isinstance(user, UserModel)

        return users


class SQLAlchemyUsersStatisticsRepository(SQLAlchemyAbstractRepository, UsersStatisticsRepository):

    async def get(self, id: int) -> Optional[UserStatisticsModel]:
        result: Result = await self._session.execute(select(UserStatisticsModel).filter_by(id=id))
        return result.scalar_one_or_none()

    async def get_by_user_id(self, user_id: int) -> Optional[UserStatisticsModel]:
        result: Result = await self._session.execute(select(UserStatisticsModel).filter_by(user_id=user_id))
        return result.scalar_one_or_none()

    async def add(self, model: AbstractModel) -> UserStatisticsModel:
        result: Result = await self._session.execute(
            insert(UserStatisticsModel).values(**await model.to_dict(exclude={'id'})).returning(UserStatisticsModel)
        )

        return result.scalar_one()

    async def update(self, id: int, model: AbstractModel) -> UserStatisticsModel:
        result: Result = await self._session.execute(
            update(
                UserStatisticsModel
            ).filter_by(
                id=id
            ).values(
                **await model.to_dict(exclude={'id'})
            ).returning(
                UserStatisticsModel
            )
        )

        return result.scalar_one()

    async def delete(self, id: int) -> None:
        await self._session.execute(delete(UserStatisticsModel).filter_by(id=id))

    async def list(self) -> List[UserStatisticsModel]:
        result: Result = await self._session.execute(select(UserStatisticsModel))
        users_statistics: Sequence[Row | RowMapping | Any] = result.scalars().all()

        assert isinstance(users_statistics, List)
        for statistics in users_statistics:
            assert isinstance(statistics, UserStatisticsModel)

        return users_statistics


class SQLAlchemyUsersVotesRepository(SQLAlchemyAbstractRepository, UsersVotesRepository):

    async def get(self, id: int) -> Optional[UserVoteModel]:
        result: Result = await self._session.execute(select(UserVoteModel).filter_by(id=id))
        return result.scalar_one_or_none()

    async def get_by_voted_for_user_id_and_voting_user_id(
            self,
            voted_for_user_id: int,
            voting_user_id: int
    ) -> Optional[UserVoteModel]:

        result: Result = await self._session.execute(
            select(UserVoteModel).filter_by(voted_for_user_id=voted_for_user_id, voting_user_id=voting_user_id)
        )
        return result.scalar_one_or_none()

    async def add(self, model: AbstractModel) -> UserVoteModel:
        result: Result = await self._session.execute(
            insert(UserVoteModel).values(**await model.to_dict(exclude={'id'})).returning(UserVoteModel)
        )

        return result.scalar_one()

    async def update(self, id: int, model: AbstractModel) -> UserVoteModel:
        result: Result = await self._session.execute(
            update(
                UserVoteModel
            ).filter_by(
                id=id
            ).values(
                **await model.to_dict(exclude={'id'})
            ).returning(
                UserVoteModel
            )
        )

        return result.scalar_one()

    async def delete(self, id: int) -> None:
        await self._session.execute(delete(UserVoteModel).filter_by(id=id))

    async def list(self) -> List[UserVoteModel]:
        result: Result = await self._session.execute(select(UserVoteModel))
        users_votes: Sequence[Row | RowMapping | Any] = result.scalars().all()

        assert isinstance(users_votes, List)
        for vote in users_votes:
            assert isinstance(vote, UserVoteModel)

        return users_votes
