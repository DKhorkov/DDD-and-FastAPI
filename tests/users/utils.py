from src.users.domain.models import UserModel, UserStatisticsModel
from src.users.interfaces import UsersRepository, UsersStatisticsRepository
from src.users.utils import hash_password
from tests.config import FakeUserConfig
from tests.users.fake_objects import FakeUsersRepository, FakeUsersStatisticsRepository


async def create_fake_users_repository_instance(with_user: bool = False) -> UsersRepository:
    users_repository: UsersRepository
    if with_user:
        user_id: int = 1
        user_data: FakeUserConfig = FakeUserConfig()
        user_data.PASSWORD = await hash_password(user_data.PASSWORD)
        user: UserModel = UserModel(**user_data.to_dict(to_lower=True), id=user_id)
        users_repository = FakeUsersRepository(users={user_id: user})
    else:
        users_repository = FakeUsersRepository()

    return users_repository


async def create_fake_users_statistics_repository_instance(with_user: bool = False) -> UsersStatisticsRepository:
    users_statistics_repository: UsersStatisticsRepository
    if with_user:
        statistics_id: int = 1
        user_id: int = 1
        users_statistics: UserStatisticsModel = UserStatisticsModel(id=statistics_id, user_id=user_id)
        users_statistics_repository = FakeUsersStatisticsRepository(users_statistics={statistics_id: users_statistics})
    else:
        users_statistics_repository = FakeUsersStatisticsRepository()

    return users_statistics_repository
