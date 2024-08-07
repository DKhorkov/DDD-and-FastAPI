from abc import ABC, abstractmethod
from typing import Any

from src.core.interfaces import AbstractUnitOfWork
from src.core.interfaces.commands import AbstractCommand
from src.core.interfaces.events import AbstractEvent


class AbstractEventHandler(ABC):
    """
    Abstract event handler class, from which every event handler should be inherited from.
    """

    @abstractmethod
    def __init__(self, uow: AbstractUnitOfWork) -> None:
        raise NotImplementedError

    @abstractmethod
    async def __call__(self, event: AbstractEvent) -> None:
        raise NotImplementedError


class AbstractCommandHandler(ABC):
    """
    Abstract command handler class, from which every command handler should be inherited from.
    """

    @abstractmethod
    def __init__(self, uow: AbstractUnitOfWork) -> None:
        raise NotImplementedError

    @abstractmethod
    async def __call__(self, command: AbstractCommand) -> Any:
        raise NotImplementedError
