from sqlalchemy import Table, Column, Integer, String, ForeignKey

from src.core.database.metadata import mapper_registry


users_table = Table(
    'users',
    mapper_registry.metadata,
    Column('id', Integer, primary_key=True, autoincrement=True, nullable=False, unique=True),
    Column('email', String, nullable=False, unique=True),
    Column('password', String, nullable=False),
    Column('username', String, nullable=False, unique=True),
)

users_statistics_table = Table(
    'users_statistics',
    mapper_registry.metadata,
    Column('id', Integer, primary_key=True, autoincrement=True, nullable=False, unique=True),
    Column(
        'user_id',
        Integer,
        ForeignKey('users.id', onupdate='CASCADE', ondelete='CASCADE'),
        nullable=False
    ),
    Column('likes', Integer, nullable=False, default=0),
    Column('dislikes', Integer, nullable=False, default=0),
)

users_votes_table = Table(
    'users_votes',
    mapper_registry.metadata,
    Column('id', Integer, primary_key=True, autoincrement=True, nullable=False, unique=True),
    Column(
        'voted_for_user_id',
        Integer,
        ForeignKey('users.id', onupdate='CASCADE', ondelete='CASCADE'),
        nullable=False
    ),
    Column(
        'voting_user_id',
        Integer,
        ForeignKey('users.id', onupdate='CASCADE', ondelete='CASCADE'),
        nullable=False
    )
)


def start_mappers():
    """
    Map all domain models to ORM models, for purpose of using domain models directly during work with the database,
    according to DDD.
    """

    # Imports here not to ruin alembic logics. Also, only for mappers they needed:
    from src.users.domain.models import UserModel, UserStatisticsModel, UserVoteModel

    mapper_registry.map_imperatively(class_=UserModel, local_table=users_table)
    mapper_registry.map_imperatively(class_=UserStatisticsModel, local_table=users_statistics_table)
    mapper_registry.map_imperatively(class_=UserVoteModel, local_table=users_votes_table)
