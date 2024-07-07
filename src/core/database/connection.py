from sqlalchemy.ext.asyncio import create_async_engine, AsyncEngine, async_sessionmaker

from src.core.database.config import database_config


"""
Due to the fact, that sqlite is serverless and has no host, port and so on, there is a need to create
database url in different patterns.
"""
DATABASE_URL: str
if database_config.DATABASE_DIALECT == 'sqlite':
    DATABASE_URL = '{}+{}:///{}'.format(
        database_config.DATABASE_DIALECT,
        database_config.DATABASE_DRIVER,
        database_config.DATABASE_NAME,
    )
else:
    DATABASE_URL = '{}+{}://{}:{}@{}:{}/{}'.format(
        database_config.DATABASE_DIALECT,
        database_config.DATABASE_DRIVER,
        database_config.DATABASE_USER,
        database_config.DATABASE_PASSWORD,
        database_config.DATABASE_HOST,
        database_config.DATABASE_PORT,
        database_config.DATABASE_NAME
    )

engine: AsyncEngine = create_async_engine(
    url=DATABASE_URL,
    pool_pre_ping=database_config.DATABASE_POOL_PRE_PING,
    pool_recycle=database_config.DATABASE_POOL_RECYCLE,
    echo=database_config.DATABASE_ECHO,
)

session_factory: async_sessionmaker = async_sessionmaker(
    bind=engine,
    autoflush=database_config.DATABASE_AUTO_FLUSH,
    expire_on_commit=database_config.DATABASE_EXPIRE_ON_COMMIT
)
