from sqlalchemy.orm import mapped_column, Mapped
from sqlalchemy import String, Integer, ForeignKey

from src.core.database.base import Base


class UserModel(Base):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(String, unique=True)
    password: Mapped[str] = mapped_column(String)
    username: Mapped[str] = mapped_column(String, unique=True)


class UserStatisticsModel(Base):
    __tablename__ = 'users_statistics'

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey('users.id', onupdate='CASCADE', ondelete='CASCADE'),
        nullable=False
    )
    likes: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    dislikes: Mapped[int] = mapped_column(Integer, nullable=False, default=0)


class UserVoteModel(Base):
    __tablename__ = 'users_votes'

    id: Mapped[int] = mapped_column(primary_key=True)
    voted_for_user_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey('users.id', onupdate='CASCADE', ondelete='CASCADE'),
        nullable=False
    )
    voting_user_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey('users.id', onupdate='CASCADE', ondelete='CASCADE'),
        nullable=False
    )
