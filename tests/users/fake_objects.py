from typing import Dict, Optional, List

from src.users.interfaces.units_of_work import UsersUnitOfWork
from src.users.interfaces.repositories import UsersRepository, UsersStatisticsRepository, UsersVotesRepository
from src.users.domain.models import UserModel, UserStatisticsModel, UserVoteModel
from src.core.interfaces import AbstractModel


class FakeUsersRepository(UsersRepository):

    def __init__(self, users: Optional[Dict[int, UserModel]] = None) -> None:
        self.users: Dict[int, UserModel] = users if users else {}

    async def get(self, id: int) -> Optional[UserModel]:
        return self.users.get(id)

    async def get_by_email(self, email: str) -> Optional[UserModel]:
        for user in self.users.values():
            if user.email == email:
                return user

        return None

    async def get_by_username(self, username: str) -> Optional[UserModel]:
        for user in self.users.values():
            if user.username == username:
                return user

        return None

    async def add(self, model: AbstractModel) -> UserModel:
        user: UserModel = UserModel(**await model.to_dict())
        self.users[user.id] = user
        return user

    async def update(self, id: int, model: AbstractModel) -> UserModel:
        user: UserModel = UserModel(**await model.to_dict())
        if id in self.users:
            self.users[id] = user

        return user

    async def delete(self, id: int) -> None:
        if id in self.users:
            del self.users[id]

    async def list(self) -> List[UserModel]:
        return list(self.users.values())


class FakeUsersStatisticsRepository(UsersStatisticsRepository):

    def __init__(self, users_statistics: Optional[Dict[int, UserStatisticsModel]] = None) -> None:
        self.users_statistics: Dict[int, UserStatisticsModel] = users_statistics if users_statistics else {}

    async def get(self, id: int) -> Optional[UserStatisticsModel]:
        return self.users_statistics.get(id)

    async def get_by_user_id(self, user_id: int) -> Optional[UserStatisticsModel]:
        for statistics in self.users_statistics.values():
            if statistics.user_id == user_id:
                return statistics

        return None

    async def add(self, model: AbstractModel) -> UserStatisticsModel:
        statistics: UserStatisticsModel = UserStatisticsModel(**await model.to_dict())
        self.users_statistics[statistics.id] = statistics
        return statistics

    async def update(self, id: int, model: AbstractModel) -> UserStatisticsModel:
        statistics: UserStatisticsModel = UserStatisticsModel(**await model.to_dict())
        if id in self.users_statistics:
            self.users_statistics[id] = statistics

        return statistics

    async def delete(self, id: int) -> None:
        if id in self.users_statistics:
            del self.users_statistics[id]

    async def list(self) -> List[UserStatisticsModel]:
        return list(self.users_statistics.values())


class FakeUsersVotesRepository(UsersVotesRepository):

    def __init__(self, users_votes: Optional[Dict[int, UserVoteModel]] = None) -> None:
        self.users_votes: Dict[int, UserVoteModel] = users_votes if users_votes else {}

    async def get(self, id: int) -> Optional[UserVoteModel]:
        return self.users_votes.get(id)

    async def get_by_voted_for_user_id_and_voting_user_id(
            self,
            voted_for_user_id: int,
            voting_user_id: int
    ) -> Optional[UserVoteModel]:

        for vote in self.users_votes.values():
            if vote.voting_user_id == voting_user_id and vote.voted_for_user_id == voted_for_user_id:
                return vote

        return None

    async def add(self, model: AbstractModel) -> UserVoteModel:
        vote: UserVoteModel = UserVoteModel(**await model.to_dict())
        self.users_votes[vote.id] = vote
        return vote

    async def update(self, id: int, model: AbstractModel) -> UserVoteModel:
        vote: UserVoteModel = UserVoteModel(**await model.to_dict())
        if id in self.users_votes:
            self.users_votes[id] = vote

        return vote

    async def delete(self, id: int) -> None:
        if id in self.users_votes:
            del self.users_votes[id]

    async def list(self) -> List[UserVoteModel]:
        return list(self.users_votes.values())


class FakeUsersUnitOfWork(UsersUnitOfWork):

    def __init__(
            self,
            users_repository: UsersRepository,
            users_statistics_repository: UsersStatisticsRepository,
            users_votes_repository: UsersVotesRepository
    ) -> None:

        super().__init__()
        self.users: UsersRepository = users_repository
        self.users_statistics: UsersStatisticsRepository = users_statistics_repository
        self.users_votes: UsersVotesRepository = users_votes_repository
        self.committed: bool = False

    async def commit(self) -> None:
        self.committed = True

    async def rollback(self) -> None:
        pass
