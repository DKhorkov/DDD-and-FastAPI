from abc import ABC
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.interfaces import AbstractRepository


class SQLAlchemyAbstractRepository(AbstractRepository, ABC):
    """
    Repository interface for SQLAlchemy, from which should be inherited all other repositories,
    which would be based on SQLAlchemy logics.
    """

    def __init__(self, session: AsyncSession) -> None:
        self._session: AsyncSession = session
