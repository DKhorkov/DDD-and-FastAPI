from abc import ABC

from src.core.interfaces.handlers import AbstractEventHandler, AbstractCommandHandler
from src.users.interfaces import UsersUnitOfWork


class UsersEventHandler(AbstractEventHandler, ABC):
    """
    Abstract event handler class, from which every users event handler should be inherited from.
    """

    def __init__(self, uow: UsersUnitOfWork) -> None:
        self._uow: UsersUnitOfWork = uow


class UsersCommandHandler(AbstractCommandHandler, ABC):
    """
    Abstract command handler class, from which every users command handler should be inherited from.
    """

    def __init__(self, uow: UsersUnitOfWork) -> None:
        self._uow: UsersUnitOfWork = uow
