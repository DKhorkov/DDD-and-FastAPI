from abc import ABC

from src.users.interfaces.repositories import UsersRepository, UsersStatisticsRepository, UsersVotesRepository
from src.core.interfaces import AbstractUnitOfWork


class UsersUnitOfWork(AbstractUnitOfWork, ABC):
    """
    An interface for work with users, that is used by service layer of users module.
    The main goal is that implementations of this interface can be easily replaced in the service layer
    using dependency injection without disrupting its functionality.
    """

    users: UsersRepository
    users_statistics: UsersStatisticsRepository
    users_votes: UsersVotesRepository
