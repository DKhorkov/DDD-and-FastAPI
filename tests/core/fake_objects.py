from dataclasses import dataclass
from typing import Any

from src.core.interfaces import (
    AbstractModel,
    AbstractCommand,
    AbstractEvent,
    AbstractEventHandler,
    AbstractCommandHandler,
    AbstractUnitOfWork
)


@dataclass
class FakeModel(AbstractModel):
    """
    Inherited model from base just to test AbstractModel's methods.
    """

    field1: str = 'test'
    field2: int = 123


@dataclass(frozen=True)
class FakeEvent(AbstractEvent):
    """
    Inherited event from base just to test AbstractEvent's methods.
    """

    field1: str = 'test'
    field2: int = 123


@dataclass(frozen=True)
class FakeCommand(AbstractCommand):
    """
    Inherited command from base just to test AbstractCommand's methods.
    """

    field1: str = 'test'
    field2: int = 123


class FakeEventHandler(AbstractEventHandler):

    def __init__(self, uow: AbstractUnitOfWork, field1: str, field2: int, create_recursion_event: bool = False) -> None:
        self.uow = uow
        self.field1: str = field1
        self.field2: int = field2
        self.create_recursion_event: bool = create_recursion_event

        self.called: bool = False

    async def __call__(self, event: AbstractEvent) -> None:
        self.called = True
        if self.create_recursion_event:
            await self.uow.add_event(FakeEvent())

    def __hash__(self) -> int:
        return hash(f'{self.field1}_{self.field2}_{self.uow}')

    def __eq__(self, other: Any) -> bool:
        return hash(self) == hash(other)


class FakeCommandHandler(AbstractCommandHandler):

    def __init__(self, uow: AbstractUnitOfWork, field1: str, field2: int) -> None:
        self.uow = uow
        self.field1: str = field1
        self.field2: int = field2

        self.called: bool = False

    async def __call__(self, command: AbstractCommand) -> None:
        self.called = True
        await self.uow.add_event(FakeEvent())

    def __hash__(self) -> int:
        return hash(f'{self.field1}_{self.field2}_{self.uow}')

    def __eq__(self, other: Any) -> bool:
        return hash(self) == hash(other)


class FakeCoreUnitOfWork(AbstractUnitOfWork):

    def __init__(self) -> None:
        super().__init__()
        self.committed: bool = False

    async def commit(self) -> None:
        self.committed = True

    async def rollback(self) -> None:
        pass
