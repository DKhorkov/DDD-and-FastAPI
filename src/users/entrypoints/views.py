from typing import List

from src.users.domain.models import UserModel, UserStatisticsModel
from src.users.interfaces.units_of_work import UsersUnitOfWork
from src.users.service_layer.service import UsersService


class UsersViews:
    """
    Views related to users, which purpose is to return information upon read requests,
    due to the fact that write requests (represented by commands) are different from read requests.

    # TODO At current moment uses repositories pattern to retrieve data. In future can be changed on raw SQL
    # TODO for speed-up purpose
    """

    def __init__(self, uow: UsersUnitOfWork) -> None:
        self._uow: UsersUnitOfWork = uow

    async def get_user_account(self, user_id: int) -> UserModel:
        users_service: UsersService = UsersService(self._uow)
        user: UserModel = await users_service.get_user_by_id(id=user_id)
        return user

    async def get_user_statistics(self, user_id: int) -> UserStatisticsModel:
        users_service: UsersService = UsersService(self._uow)
        user_statistics: UserStatisticsModel = await users_service.get_user_statistics_by_user_id(user_id=user_id)
        return user_statistics

    async def get_all_users(self) -> List[UserModel]:
        users_service: UsersService = UsersService(self._uow)
        users: List[UserModel] = await users_service.get_all_users()
        return users
