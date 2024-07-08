import pytest
from typing import Optional, List, Sequence
from sqlalchemy import select, CursorResult, Row, insert, RowMapping
from sqlalchemy.exc import IntegrityError, NoResultFound
from sqlalchemy.ext.asyncio import AsyncConnection, AsyncSession, async_sessionmaker, create_async_engine, AsyncEngine

from src.core.database.connection import DATABASE_URL
from src.users.domain.models import UserModel, UserStatisticsModel, UserVoteModel
from src.users.adapters.repositories import (
    SQLAlchemyUsersRepository,
    SQLAlchemyUsersVotesRepository,
    SQLAlchemyUsersStatisticsRepository
)
from tests.config import FakeUserConfig


@pytest.mark.anyio
async def test_sqlalchemy_users_repository_get_success(
        create_test_user: None,
        async_connection: AsyncConnection
) -> None:

    async_session_factory: async_sessionmaker = async_sessionmaker(bind=async_connection)
    session: AsyncSession = async_session_factory()
    user: Optional[UserModel] = await SQLAlchemyUsersRepository(session=session).get(id=1)

    assert user is not None
    assert user.id == 1
    assert user.email == FakeUserConfig.EMAIL
    assert user.username == FakeUserConfig.USERNAME


@pytest.mark.anyio
async def test_sqlalchemy_users_repository_get_fail(
        create_test_user: None,
        async_connection: AsyncConnection
) -> None:

    async_session_factory: async_sessionmaker = async_sessionmaker(bind=async_connection)
    session: AsyncSession = async_session_factory()
    user: Optional[UserModel] = await SQLAlchemyUsersRepository(session=session).get(id=2)
    assert user is None


@pytest.mark.anyio
async def test_sqlalchemy_users_repository_get_by_email_success(
        create_test_user: None,
        async_connection: AsyncConnection
) -> None:

    async_session_factory: async_sessionmaker = async_sessionmaker(bind=async_connection)
    session: AsyncSession = async_session_factory()
    user: Optional[UserModel] = await SQLAlchemyUsersRepository(session=session).get_by_email(
        email=FakeUserConfig.EMAIL
    )

    assert user is not None
    assert user.id == 1
    assert user.email == FakeUserConfig.EMAIL
    assert user.username == FakeUserConfig.USERNAME


@pytest.mark.anyio
async def test_sqlalchemy_users_repository_get_by_email_fail(
        create_test_user: None,
        async_connection: AsyncConnection
) -> None:

    async_session_factory: async_sessionmaker = async_sessionmaker(bind=async_connection)
    session: AsyncSession = async_session_factory()
    user: Optional[UserModel] = await SQLAlchemyUsersRepository(session=session).get_by_email(
        email='non-existing-email@gmail.com'
    )

    assert user is None


@pytest.mark.anyio
async def test_sqlalchemy_users_repository_get_by_username_success(
        create_test_user: None,
        async_connection: AsyncConnection
) -> None:

    async_session_factory: async_sessionmaker = async_sessionmaker(bind=async_connection)
    session: AsyncSession = async_session_factory()
    user: Optional[UserModel] = await SQLAlchemyUsersRepository(session=session).get_by_username(
        username=FakeUserConfig.USERNAME
    )

    assert user is not None
    assert user.id == 1
    assert user.email == FakeUserConfig.EMAIL
    assert user.username == FakeUserConfig.USERNAME


@pytest.mark.anyio
async def test_sqlalchemy_users_repository_get_by_username_fail(
        create_test_user: None,
        async_connection: AsyncConnection
) -> None:

    async_session_factory: async_sessionmaker = async_sessionmaker(bind=async_connection)
    session: AsyncSession = async_session_factory()
    user: Optional[UserModel] = await SQLAlchemyUsersRepository(session=session).get_by_username(
        username='non-existing-username'
    )

    assert user is None


@pytest.mark.anyio
async def test_sqlalchemy_users_repository_list(
        create_test_user: None,
        async_connection: AsyncConnection
) -> None:

    async_session_factory: async_sessionmaker = async_sessionmaker(bind=async_connection)
    session: AsyncSession = async_session_factory()
    users_list: List[UserModel] = await SQLAlchemyUsersRepository(session=session).list()
    assert len(users_list) == 1
    user: UserModel = users_list[0]
    assert user.id == 1
    assert user.email == FakeUserConfig.EMAIL
    assert user.username == FakeUserConfig.USERNAME


@pytest.mark.anyio
async def test_sqlalchemy_users_repository_empty_list(
        map_models_to_orm: None,
        async_connection: AsyncConnection
) -> None:

    async_session_factory: async_sessionmaker = async_sessionmaker(bind=async_connection)
    session: AsyncSession = async_session_factory()
    users_list: List[UserModel] = await SQLAlchemyUsersRepository(session=session).list()
    assert len(users_list) == 0


@pytest.mark.anyio
async def test_sqlalchemy_users_repository_delete_existing_user(
        create_test_user: None,
        async_connection: AsyncConnection
) -> None:

    cursor: CursorResult = await async_connection.execute(select(UserModel))
    result: Sequence[Row] = cursor.all()
    assert len(result) == 1

    async_session_factory: async_sessionmaker = async_sessionmaker(bind=async_connection)
    session: AsyncSession = async_session_factory()
    await SQLAlchemyUsersRepository(session=session).delete(id=1)

    cursor = await async_connection.execute(select(UserModel))
    result = cursor.all()
    assert len(result) == 0


@pytest.mark.anyio
async def test_sqlalchemy_users_repository_delete_non_existing_user(
        map_models_to_orm: None,
        async_connection: AsyncConnection
) -> None:

    cursor: CursorResult = await async_connection.execute(select(UserModel))
    result: Sequence[Row] = cursor.all()
    assert len(result) == 0

    async_session_factory: async_sessionmaker = async_sessionmaker(bind=async_connection)
    session: AsyncSession = async_session_factory()
    await SQLAlchemyUsersRepository(session=session).delete(id=1)


@pytest.mark.anyio
async def test_sqlalchemy_users_repository_add_user_success(
        map_models_to_orm: None,
        async_connection: AsyncConnection
) -> None:

    cursor: CursorResult = await async_connection.execute(select(UserModel).filter_by(email=FakeUserConfig.EMAIL))
    result: Optional[Row] = cursor.first()
    assert not result

    async_session_factory: async_sessionmaker = async_sessionmaker(bind=async_connection)
    session: AsyncSession = async_session_factory()
    user: UserModel = UserModel(**FakeUserConfig().to_dict(to_lower=True))
    await SQLAlchemyUsersRepository(session=session).add(model=user)

    cursor = await async_connection.execute(select(UserModel).filter_by(email=FakeUserConfig.EMAIL))
    result = cursor.first()
    assert result


@pytest.mark.anyio
async def test_sqlalchemy_users_repository_add_user_success_with_provided_already_existing_id(
        create_test_user: None,
        async_connection: AsyncConnection
) -> None:

    cursor: CursorResult = await async_connection.execute(select(UserModel).filter_by(id=1))
    result: Optional[Row] = cursor.first()
    assert result

    async_session_factory: async_sessionmaker = async_sessionmaker(bind=async_connection)
    session: AsyncSession = async_session_factory()
    username: str = 'someUsername'
    user: UserModel = UserModel(
        id=1,
        email='someTestEmail@gmail.com',
        username=username,
        password=FakeUserConfig.PASSWORD
    )

    await SQLAlchemyUsersRepository(session=session).add(model=user)

    cursor = await async_connection.execute(select(UserModel).filter_by(username=username))
    result = cursor.first()
    assert result


@pytest.mark.anyio
async def test_sqlalchemy_users_repository_add_user_fail_username_already_exists(
        create_test_user: None,
        async_connection: AsyncConnection
) -> None:

    cursor: CursorResult = await async_connection.execute(select(UserModel).filter_by(username=FakeUserConfig.USERNAME))
    result: Optional[Row] = cursor.first()
    assert result

    async_session_factory: async_sessionmaker = async_sessionmaker(bind=async_connection)
    session: AsyncSession = async_session_factory()
    user: UserModel = UserModel(
        username=FakeUserConfig.USERNAME,
        email='someTestEmail@gmail.com',
        password=FakeUserConfig.PASSWORD
    )

    with pytest.raises(IntegrityError):
        await SQLAlchemyUsersRepository(session=session).add(model=user)


@pytest.mark.anyio
async def test_sqlalchemy_users_repository_add_user_fail_email_already_exists(
        create_test_user: None,
        async_connection: AsyncConnection
) -> None:

    cursor: CursorResult = await async_connection.execute(select(UserModel).filter_by(email=FakeUserConfig.EMAIL))
    result: Optional[Row] = cursor.first()
    assert result

    async_session_factory: async_sessionmaker = async_sessionmaker(bind=async_connection)
    session: AsyncSession = async_session_factory()
    user: UserModel = UserModel(
        email=FakeUserConfig.EMAIL,
        username='someUsername',
        password=FakeUserConfig.PASSWORD
    )

    with pytest.raises(IntegrityError):
        await SQLAlchemyUsersRepository(session=session).add(model=user)


@pytest.mark.anyio
async def test_sqlalchemy_users_repository_update_existing_user(
        create_test_user: None,
        async_connection: AsyncConnection
) -> None:

    cursor: CursorResult = await async_connection.execute(select(UserModel).filter_by(id=1))
    result: Optional[Row] = cursor.first()
    assert result

    async_session_factory: async_sessionmaker = async_sessionmaker(bind=async_connection)
    session: AsyncSession = async_session_factory()
    username: str = 'someUsername'
    user: UserModel = UserModel(
        email=FakeUserConfig.EMAIL,
        username=username,
        password=FakeUserConfig.PASSWORD
    )

    await SQLAlchemyUsersRepository(session=session).update(id=1, model=user)

    cursor = await async_connection.execute(select(UserModel).filter_by(username=username))
    result = cursor.first()
    assert result


@pytest.mark.anyio
async def test_sqlalchemy_users_repository_update_non_existing_user(
        map_models_to_orm: None,
        async_connection: AsyncConnection
) -> None:

    cursor: CursorResult = await async_connection.execute(select(UserModel).filter_by(id=1))
    result: Optional[Row] = cursor.first()
    assert not result

    async_session_factory: async_sessionmaker = async_sessionmaker(bind=async_connection)
    session: AsyncSession = async_session_factory()
    user: UserModel = UserModel(**FakeUserConfig().to_dict(to_lower=True))
    with pytest.raises(NoResultFound):
        await SQLAlchemyUsersRepository(session=session).update(id=1, model=user)


@pytest.mark.anyio
async def test_sqlalchemy_users_statistics_repository_get_success(
        create_test_user: None,
        async_connection: AsyncConnection
) -> None:

    async_session_factory: async_sessionmaker = async_sessionmaker(bind=async_connection)
    session: AsyncSession = async_session_factory()
    user_statistics: Optional[UserStatisticsModel] = await SQLAlchemyUsersStatisticsRepository(
        session=session
    ).get(
        id=1
    )

    assert user_statistics is not None
    assert user_statistics.user_id == 1
    assert user_statistics.likes == 0
    assert user_statistics.dislikes == 0


@pytest.mark.anyio
async def test_sqlalchemy_users_statistics_repository_get_fail(
        map_models_to_orm: None,
        async_connection: AsyncConnection
) -> None:

    async_session_factory: async_sessionmaker = async_sessionmaker(bind=async_connection)
    session: AsyncSession = async_session_factory()
    user_statistics: Optional[UserStatisticsModel] = await SQLAlchemyUsersStatisticsRepository(
        session=session
    ).get(
        id=1
    )

    assert user_statistics is None


@pytest.mark.anyio
async def test_sqlalchemy_users_statistics_repository_get_by_user_id_success(
        create_test_user: None,
        async_connection: AsyncConnection
) -> None:

    async_session_factory: async_sessionmaker = async_sessionmaker(bind=async_connection)
    session: AsyncSession = async_session_factory()
    user_statistics: Optional[UserStatisticsModel] = await SQLAlchemyUsersStatisticsRepository(
        session=session
    ).get_by_user_id(
        user_id=1
    )

    assert user_statistics is not None
    assert user_statistics.user_id == 1
    assert user_statistics.likes == 0
    assert user_statistics.dislikes == 0


@pytest.mark.anyio
async def test_sqlalchemy_users_statistics_repository_get_by_user_id_fail(
        map_models_to_orm: None,
        async_connection: AsyncConnection
) -> None:

    async_session_factory: async_sessionmaker = async_sessionmaker(bind=async_connection)
    session: AsyncSession = async_session_factory()
    user_statistics: Optional[UserStatisticsModel] = await SQLAlchemyUsersStatisticsRepository(
        session=session
    ).get_by_user_id(
        user_id=1
    )

    assert user_statistics is None


@pytest.mark.anyio
async def test_sqlalchemy_users_statistics_repository_list(
        create_test_user: None,
        async_connection: AsyncConnection
) -> None:

    async_session_factory: async_sessionmaker = async_sessionmaker(bind=async_connection)
    session: AsyncSession = async_session_factory()
    users_statistics: List[UserStatisticsModel] = await SQLAlchemyUsersStatisticsRepository(session=session).list()
    assert len(users_statistics) == 1

    user_statistics: UserStatisticsModel = users_statistics[0]
    assert user_statistics is not None
    assert user_statistics.user_id == 1
    assert user_statistics.likes == 0
    assert user_statistics.dislikes == 0


@pytest.mark.anyio
async def test_sqlalchemy_users_statistics_repository_empty_list(
        map_models_to_orm: None,
        async_connection: AsyncConnection
) -> None:

    async_session_factory: async_sessionmaker = async_sessionmaker(bind=async_connection)
    session: AsyncSession = async_session_factory()
    users_statistics: List[UserStatisticsModel] = await SQLAlchemyUsersStatisticsRepository(session=session).list()
    assert len(users_statistics) == 0


@pytest.mark.anyio
async def test_sqlalchemy_users_statistics_repository_delete_existing_user_statistics(
        create_test_user: None,
        async_connection: AsyncConnection
) -> None:

    cursor: CursorResult = await async_connection.execute(select(UserStatisticsModel))
    result: Sequence[Row] = cursor.all()
    assert len(result) == 1

    async_session_factory: async_sessionmaker = async_sessionmaker(bind=async_connection)
    session: AsyncSession = async_session_factory()
    await SQLAlchemyUsersStatisticsRepository(session=session).delete(id=1)

    cursor = await async_connection.execute(select(UserStatisticsModel))
    result = cursor.all()
    assert len(result) == 0


@pytest.mark.anyio
async def test_sqlalchemy_users_statistics_repository_delete_non_existing_user_statistics(
        map_models_to_orm: None,
        async_connection: AsyncConnection
) -> None:

    cursor: CursorResult = await async_connection.execute(select(UserStatisticsModel))
    result: Sequence[Row] = cursor.all()
    assert len(result) == 0

    async_session_factory: async_sessionmaker = async_sessionmaker(bind=async_connection)
    session: AsyncSession = async_session_factory()
    await SQLAlchemyUsersStatisticsRepository(session=session).delete(id=1)


@pytest.mark.anyio
async def test_sqlalchemy_users_statistics_repository_add_user_statistics_success(
        map_models_to_orm: None,
        async_connection: AsyncConnection
) -> None:

    cursor: CursorResult = await async_connection.execute(select(UserStatisticsModel).filter_by(user_id=1))
    result: Optional[Row] = cursor.first()
    assert not result

    engine: AsyncEngine = create_async_engine(DATABASE_URL)
    async with engine.begin() as conn:
        await conn.execute(insert(UserModel).values(**FakeUserConfig().to_dict(to_lower=True)))
        await conn.commit()

    async_session_factory: async_sessionmaker = async_sessionmaker(bind=async_connection)
    session: AsyncSession = async_session_factory()
    user_statistics: UserStatisticsModel = UserStatisticsModel(user_id=1)
    await SQLAlchemyUsersStatisticsRepository(session=session).add(model=user_statistics)

    cursor = await async_connection.execute(select(UserStatisticsModel).filter_by(user_id=1))
    result = cursor.first()
    assert result


@pytest.mark.anyio
async def test_sqlalchemy_users_statistics_repository_update_existing_user_statistics(
        create_test_user: None,
        async_connection: AsyncConnection
) -> None:

    cursor: CursorResult = await async_connection.execute(select(UserStatisticsModel).filter_by(id=1))
    result: Optional[Row] = cursor.first()
    assert result

    async_session_factory: async_sessionmaker = async_sessionmaker(bind=async_connection)
    session: AsyncSession = async_session_factory()
    user_statistics: UserStatisticsModel = UserStatisticsModel(user_id=1, likes=5, dislikes=5)
    await SQLAlchemyUsersStatisticsRepository(session=session).update(id=1, model=user_statistics)

    cursor = await async_connection.execute(select(UserStatisticsModel).filter_by(user_id=1))
    final_result: Optional[RowMapping] = cursor.mappings().fetchone()
    assert final_result
    assert final_result['likes'] == 5
    assert final_result['dislikes'] == 5


@pytest.mark.anyio
async def test_sqlalchemy_users_statistics_repository_update_non_existing_user_statistics(
        map_models_to_orm: None,
        async_connection: AsyncConnection
) -> None:

    cursor: CursorResult = await async_connection.execute(select(UserStatisticsModel).filter_by(id=1))
    result: Optional[Row] = cursor.first()
    assert not result

    async_session_factory: async_sessionmaker = async_sessionmaker(bind=async_connection)
    session: AsyncSession = async_session_factory()
    user_statistics: UserStatisticsModel = UserStatisticsModel(user_id=1, likes=5, dislikes=5)
    with pytest.raises(NoResultFound):
        await SQLAlchemyUsersStatisticsRepository(session=session).update(id=1, model=user_statistics)


@pytest.mark.anyio
async def test_sqlalchemy_users_votes_repository_get_success(
        create_test_user: None,
        async_connection: AsyncConnection
) -> None:

    engine: AsyncEngine = create_async_engine(DATABASE_URL)
    async with engine.begin() as conn:
        await conn.execute(insert(UserVoteModel).values(voting_user_id=1, voted_for_user_id=1))
        await conn.commit()

    async_session_factory: async_sessionmaker = async_sessionmaker(bind=async_connection)
    session: AsyncSession = async_session_factory()
    user_votes: Optional[UserVoteModel] = await SQLAlchemyUsersVotesRepository(
        session=session
    ).get(
        id=1
    )

    assert user_votes is not None
    assert user_votes.voting_user_id == 1
    assert user_votes.voted_for_user_id == 1


@pytest.mark.anyio
async def test_sqlalchemy_users_votes_repository_get_fail(
        map_models_to_orm: None,
        async_connection: AsyncConnection
) -> None:

    async_session_factory: async_sessionmaker = async_sessionmaker(bind=async_connection)
    session: AsyncSession = async_session_factory()
    user_votes: Optional[UserVoteModel] = await SQLAlchemyUsersVotesRepository(
        session=session
    ).get(
        id=1
    )

    assert user_votes is None


@pytest.mark.anyio
async def test_sqlalchemy_users_votes_repository_get_by_user_id_success(
        create_test_user: None,
        async_connection: AsyncConnection
) -> None:

    engine: AsyncEngine = create_async_engine(DATABASE_URL)
    async with engine.begin() as conn:
        await conn.execute(insert(UserVoteModel).values(voting_user_id=1, voted_for_user_id=1))
        await conn.commit()

    async_session_factory: async_sessionmaker = async_sessionmaker(bind=async_connection)
    session: AsyncSession = async_session_factory()
    user_votes: Optional[UserVoteModel] = await SQLAlchemyUsersVotesRepository(
        session=session
    ).get_by_voted_for_user_id_and_voting_user_id(
        voting_user_id=1,
        voted_for_user_id=1
    )

    assert user_votes is not None
    assert user_votes.voting_user_id == 1
    assert user_votes.voted_for_user_id == 1


@pytest.mark.anyio
async def test_sqlalchemy_users_votes_repository_get_by_user_id_fail(
        map_models_to_orm: None,
        async_connection: AsyncConnection
) -> None:

    async_session_factory: async_sessionmaker = async_sessionmaker(bind=async_connection)
    session: AsyncSession = async_session_factory()
    user_votes: Optional[UserVoteModel] = await SQLAlchemyUsersVotesRepository(
        session=session
    ).get_by_voted_for_user_id_and_voting_user_id(
        voting_user_id=1,
        voted_for_user_id=1
    )

    assert user_votes is None


@pytest.mark.anyio
async def test_sqlalchemy_users_votes_repository_list(
        create_test_user: None,
        async_connection: AsyncConnection
) -> None:

    engine: AsyncEngine = create_async_engine(DATABASE_URL)
    async with engine.begin() as conn:
        await conn.execute(insert(UserVoteModel).values(voting_user_id=1, voted_for_user_id=1))
        await conn.commit()

    async_session_factory: async_sessionmaker = async_sessionmaker(bind=async_connection)
    session: AsyncSession = async_session_factory()
    users_votes: List[UserVoteModel] = await SQLAlchemyUsersVotesRepository(session=session).list()
    assert len(users_votes) == 1

    user_votes: UserVoteModel = users_votes[0]
    assert user_votes is not None
    assert user_votes.voting_user_id == 1
    assert user_votes.voted_for_user_id == 1


@pytest.mark.anyio
async def test_sqlalchemy_users_votes_repository_empty_list(
        map_models_to_orm: None,
        async_connection: AsyncConnection
) -> None:

    async_session_factory: async_sessionmaker = async_sessionmaker(bind=async_connection)
    session: AsyncSession = async_session_factory()
    users_votes: List[UserVoteModel] = await SQLAlchemyUsersVotesRepository(session=session).list()
    assert len(users_votes) == 0


@pytest.mark.anyio
async def test_sqlalchemy_users_votes_repository_delete_existing_user_votes(
        create_test_user: None,
        async_connection: AsyncConnection
) -> None:

    engine: AsyncEngine = create_async_engine(DATABASE_URL)
    async with engine.begin() as conn:
        await conn.execute(insert(UserVoteModel).values(voting_user_id=1, voted_for_user_id=1))
        await conn.commit()

    cursor: CursorResult = await async_connection.execute(select(UserVoteModel))
    result: Sequence[Row] = cursor.all()
    assert len(result) == 1

    async_session_factory: async_sessionmaker = async_sessionmaker(bind=async_connection)
    session: AsyncSession = async_session_factory()
    await SQLAlchemyUsersVotesRepository(session=session).delete(id=1)

    cursor = await async_connection.execute(select(UserVoteModel))
    result = cursor.all()
    assert len(result) == 0


@pytest.mark.anyio
async def test_sqlalchemy_users_votes_repository_delete_non_existing_user_votes(
        map_models_to_orm: None,
        async_connection: AsyncConnection
) -> None:

    cursor: CursorResult = await async_connection.execute(select(UserVoteModel))
    result: Sequence[Row] = cursor.all()
    assert len(result) == 0

    async_session_factory: async_sessionmaker = async_sessionmaker(bind=async_connection)
    session: AsyncSession = async_session_factory()
    await SQLAlchemyUsersVotesRepository(session=session).delete(id=1)


@pytest.mark.anyio
async def test_sqlalchemy_users_votes_repository_add_user_votes_success(
        map_models_to_orm: None,
        async_connection: AsyncConnection
) -> None:

    cursor: CursorResult = await async_connection.execute(select(UserVoteModel).filter_by(id=1))
    result: Optional[Row] = cursor.first()
    assert not result

    engine: AsyncEngine = create_async_engine(DATABASE_URL)
    async with engine.begin() as conn:
        await conn.execute(insert(UserModel).values(**FakeUserConfig().to_dict(to_lower=True)))
        await conn.commit()

    async_session_factory: async_sessionmaker = async_sessionmaker(bind=async_connection)
    session: AsyncSession = async_session_factory()
    user_vote: UserVoteModel = UserVoteModel(voting_user_id=1, voted_for_user_id=1)
    await SQLAlchemyUsersVotesRepository(session=session).add(model=user_vote)

    cursor = await async_connection.execute(select(UserVoteModel).filter_by(id=1))
    result = cursor.first()
    assert result


@pytest.mark.anyio
async def test_sqlalchemy_users_votes_repository_update_existing_user_votes(
        create_test_user: None,
        async_connection: AsyncConnection
) -> None:

    engine: AsyncEngine = create_async_engine(DATABASE_URL)
    async with engine.begin() as conn:
        await conn.execute(insert(UserVoteModel).values(voting_user_id=1, voted_for_user_id=1))
        await conn.commit()

    cursor: CursorResult = await async_connection.execute(select(UserVoteModel).filter_by(id=1))
    result: Optional[Row] = cursor.first()
    assert result

    async_session_factory: async_sessionmaker = async_sessionmaker(bind=async_connection)
    session: AsyncSession = async_session_factory()
    user_vote: UserVoteModel = UserVoteModel(voting_user_id=1, voted_for_user_id=1)
    await SQLAlchemyUsersVotesRepository(session=session).update(id=1, model=user_vote)

    cursor = await async_connection.execute(select(UserVoteModel).filter_by(id=1))
    result = cursor.first()
    assert result


@pytest.mark.anyio
async def test_sqlalchemy_users_votes_repository_update_non_existing_user_votes(
        map_models_to_orm: None,
        async_connection: AsyncConnection
) -> None:

    cursor: CursorResult = await async_connection.execute(select(UserVoteModel).filter_by(id=1))
    result: Optional[Row] = cursor.first()
    assert not result

    async_session_factory: async_sessionmaker = async_sessionmaker(bind=async_connection)
    session: AsyncSession = async_session_factory()
    user_vote: UserVoteModel = UserVoteModel(voting_user_id=1, voted_for_user_id=1)
    with pytest.raises(NoResultFound):
        await SQLAlchemyUsersVotesRepository(session=session).update(id=1, model=user_vote)
