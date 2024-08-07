from typing import Self

from src.users.interfaces.repositories import UsersRepository, UsersStatisticsRepository, UsersVotesRepository
from src.users.interfaces.units_of_work import UsersUnitOfWork
from src.users.adapters.repositories import (
    SQLAlchemyUsersRepository,
    SQLAlchemyUsersStatisticsRepository,
    SQLAlchemyUsersVotesRepository
)
from src.core.database.interfaces.units_of_work import SQLAlchemyAbstractUnitOfWork


class SQLAlchemyUsersUnitOfWork(SQLAlchemyAbstractUnitOfWork, UsersUnitOfWork):

    async def __aenter__(self) -> Self:
        uow = await super().__aenter__()
        self.users: UsersRepository = SQLAlchemyUsersRepository(session=self._session)
        self.users_statistics: UsersStatisticsRepository = SQLAlchemyUsersStatisticsRepository(session=self._session)
        self.users_votes: UsersVotesRepository = SQLAlchemyUsersVotesRepository(session=self._session)
        return uow
