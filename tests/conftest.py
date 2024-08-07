import pytest
import os

from celery import Celery
from httpx import AsyncClient, Cookies, Response
from sqlalchemy import insert, CursorResult, RowMapping
from sqlalchemy.ext.asyncio import create_async_engine, AsyncEngine, AsyncConnection
from sqlalchemy.exc import ArgumentError, IntegrityError
from typing import AsyncGenerator, Optional

from src.app import app
from src.users.config import RouterConfig, URLPathsConfig, cookies_config
from src.users.domain.models import UserModel, UserStatisticsModel
from src.core.database.connection import DATABASE_URL
from src.core.database.metadata import metadata
from src.users.adapters.orm import start_mappers as start_users_mappers
from src.users.utils import hash_password
from src.celery.celery_app import celery
from tests.config import FakeUserConfig
from tests.utils import get_base_url, drop_test_db


@pytest.fixture(scope='session')
def anyio_backend() -> str:
    """
    Launch tests only on "asyncio" backend, without "trio" backend.
    """

    return 'asyncio'


@pytest.fixture
async def async_connection() -> AsyncGenerator[AsyncConnection, None]:
    engine: AsyncEngine = create_async_engine(DATABASE_URL)
    async with engine.begin() as conn:
        yield conn


@pytest.fixture
async def create_test_db(async_connection: AsyncConnection) -> AsyncGenerator[None, None]:
    await async_connection.run_sync(metadata.create_all)
    yield
    drop_test_db()


@pytest.fixture
async def map_models_to_orm(create_test_db: None) -> None:
    """
    Create mappings from models to ORM according to DDD.
    """

    try:
        start_users_mappers()
    except ArgumentError:
        pass


@pytest.fixture
async def async_client(map_models_to_orm: None) -> AsyncGenerator[AsyncClient, None]:
    """
    Creates test app client for end-to-end tests to make requests to endpoints with.
    """

    async with AsyncClient(app=app, base_url=get_base_url()) as async_client:
        yield async_client


@pytest.fixture
async def create_test_user(map_models_to_orm: None) -> None:
    """
    Creates test user in test database, if user with provided credentials does not exist.
    """

    engine: AsyncEngine = create_async_engine(DATABASE_URL)
    test_user_config: FakeUserConfig = FakeUserConfig()
    test_user_config.PASSWORD = await hash_password(test_user_config.PASSWORD)
    async with engine.begin() as conn:
        try:
            cursor: CursorResult = await conn.execute(
                insert(UserModel).values(**test_user_config.to_dict(to_lower=True)).returning(UserModel)
            )
            user_data: Optional[RowMapping] = cursor.mappings().fetchone()
            assert user_data is not None
            user: UserModel = UserModel(**user_data)
            await conn.execute(insert(UserStatisticsModel).values(user_id=user.id))
            await conn.commit()
        except IntegrityError:
            await conn.rollback()


@pytest.fixture
async def access_token(async_client: AsyncClient, create_test_user: None) -> str:
    """
    Gets access token for test user, for usage during end-to-end tests to make request,
    which requires authenticated user.
    """

    response: Response = await async_client.post(
        url=RouterConfig.PREFIX + URLPathsConfig.LOGIN,
        json=FakeUserConfig().to_dict(to_lower=True)
    )
    access_token: str = response.cookies[cookies_config.COOKIES_KEY]
    return access_token


@pytest.fixture
async def cookies(access_token: str) -> Cookies:
    """
    Creates cookies object for AsyncClient, for usage during end-to-end tests to make request,
    which requires authenticated user.
    """

    cookies: Cookies = Cookies()
    domain: str = os.environ.get('HOST', '0.0.0.0')
    cookies.set(name=cookies_config.COOKIES_KEY, value=access_token, domain=domain)
    return cookies


@pytest.fixture
def celery_app() -> Celery:
    celery.conf.update(CELERY_ALWAYS_EAGER=True)
    return celery
