from abc import ABC, abstractmethod
from typing import List, Optional

from src.core.interfaces.models import AbstractModel


class AbstractRepository(ABC):
    """
    Interface for any repository, which would be used for work with domain model, according DDD.

    Main purpose is to encapsulate internal logic that is associated with the use of one or another data
    storage scheme, for example, ORM.
    """

    @abstractmethod
    async def add(self, model: AbstractModel) -> AbstractModel:
        raise NotImplementedError

    @abstractmethod
    async def get(self, id: int) -> Optional[AbstractModel]:
        raise NotImplementedError

    @abstractmethod
    async def update(self, id: int, model: AbstractModel) -> AbstractModel:
        raise NotImplementedError

    @abstractmethod
    async def delete(self, id: int) -> None:
        raise NotImplementedError

    @abstractmethod
    async def list(self) -> List[AbstractModel]:
        raise NotImplementedError
