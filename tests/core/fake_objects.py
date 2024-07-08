from dataclasses import dataclass

from src.core.interfaces import (
    AbstractModel,
    AbstractUnitOfWork
)


@dataclass
class FakeModel(AbstractModel):
    """
    Inherited model from base just to test AbstractModel's methods.
    """

    field1: str = 'test'
    field2: int = 123


class FakeCoreUnitOfWork(AbstractUnitOfWork):

    def __init__(self) -> None:
        super().__init__()
        self.committed: bool = False

    async def commit(self) -> None:
        self.committed = True

    async def rollback(self) -> None:
        pass
