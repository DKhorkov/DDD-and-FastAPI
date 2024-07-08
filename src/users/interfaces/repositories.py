from typing import Optional, List
from abc import ABC, abstractmethod

from src.core.interfaces import AbstractRepository, AbstractModel
from src.users.domain.models import UserModel, UserStatisticsModel, UserVoteModel


class UsersRepository(AbstractRepository, ABC):
    """
    An interface for work with users, that is used by users unit of work.
    The main goal is that implementations of this interface can be easily replaced in users unit of work
    using dependency injection without disrupting its functionality.
    """

    @abstractmethod
    async def get_by_email(self, email: str) -> Optional[UserModel]:
        raise NotImplementedError

    @abstractmethod
    async def get_by_username(self, username: str) -> Optional[UserModel]:
        raise NotImplementedError

    @abstractmethod
    async def add(self, model: AbstractModel) -> UserModel:
        raise NotImplementedError

    @abstractmethod
    async def get(self, id: int) -> Optional[UserModel]:
        raise NotImplementedError

    @abstractmethod
    async def update(self, id: int, model: AbstractModel) -> UserModel:
        raise NotImplementedError

    @abstractmethod
    async def list(self) -> List[UserModel]:
        raise NotImplementedError


class UsersStatisticsRepository(AbstractRepository, ABC):

    @abstractmethod
    async def add(self, model: AbstractModel) -> UserStatisticsModel:
        raise NotImplementedError

    @abstractmethod
    async def get(self, id: int) -> Optional[UserStatisticsModel]:
        raise NotImplementedError

    @abstractmethod
    async def get_by_user_id(self, user_id: int) -> Optional[UserStatisticsModel]:
        raise NotImplementedError

    @abstractmethod
    async def update(self, id: int, model: AbstractModel) -> UserStatisticsModel:
        raise NotImplementedError

    @abstractmethod
    async def list(self) -> List[UserStatisticsModel]:
        raise NotImplementedError


class UsersVotesRepository(AbstractRepository, ABC):

    @abstractmethod
    async def add(self, model: AbstractModel) -> UserVoteModel:
        raise NotImplementedError

    @abstractmethod
    async def get(self, id: int) -> Optional[UserVoteModel]:
        raise NotImplementedError

    @abstractmethod
    async def get_by_voted_for_user_id_and_voting_user_id(
            self,
            voted_for_user_id: int,
            voting_user_id: int
    ) -> Optional[UserVoteModel]:

        raise NotImplementedError

    @abstractmethod
    async def update(self, id: int, model: AbstractModel) -> UserVoteModel:
        raise NotImplementedError

    @abstractmethod
    async def list(self) -> List[UserVoteModel]:
        raise NotImplementedError
