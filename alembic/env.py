from logging.config import fileConfig

from sqlalchemy import engine_from_config
from sqlalchemy import pool

from alembic import context

from src.core.database.base import Base

import os
from pathlib import Path
from dotenv import dotenv_values
from typing import Dict


# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
config = context.config

# Interpret the config file for Python logging.
# This line sets up loggers basically.
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# add your model's MetaData object here
# for 'autogenerate' support
target_metadata = Base.metadata

# other values from the config, defined by the needs of env.py,
# can be acquired:
# my_important_option = config.get_main_option("my_important_option")
# ... etc.

# Reading environments from file:
DOTENV: Path = Path(f'{os.getcwd()}/.env')

# Creating database url and changes async driver to sync, if needed:
DATABASE_CONFIG: Dict[str, str] = dotenv_values(DOTENV)
DATABASE_DIALECT: str = DATABASE_CONFIG['DATABASE_DIALECT']
DATABASE_DRIVER: str = DATABASE_CONFIG['DATABASE_DRIVER']
if DATABASE_DRIVER.startswith('a'):  # asyncpg or other async driver
    DATABASE_DRIVER_AND_DIALECT = DATABASE_DIALECT
else:
    DATABASE_DRIVER_AND_DIALECT = DATABASE_DIALECT + '+' + DATABASE_DRIVER

DATABASE_URL: str
if DATABASE_CONFIG['DATABASE_DIALECT'] == 'sqlite':
    DATABASE_URL = '{}:///{}'.format(
        DATABASE_DRIVER_AND_DIALECT,
        DATABASE_CONFIG['DATABASE_DRIVER'],
        DATABASE_CONFIG['DATABASE_NAME'],
    )
else:
    DATABASE_URL = '{}://{}:{}@{}:{}/{}'.format(
        DATABASE_DRIVER_AND_DIALECT,
        DATABASE_CONFIG['DATABASE_USER'],
        DATABASE_CONFIG['DATABASE_PASSWORD'],
        DATABASE_CONFIG['DATABASE_HOST'],
        DATABASE_CONFIG['DATABASE_PORT'],
        DATABASE_CONFIG['DATABASE_NAME']
    )

# Setting database url for alembic correct work:
config.set_main_option("sqlalchemy.url", DATABASE_URL)
config.compare_type = True
config.compare_server_default = True


def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode.

    This configures the context with just a URL
    and not an Engine, though an Engine is acceptable
    here as well.  By skipping the Engine creation
    we don't even need a DBAPI to be available.

    Calls to context.execute() here emit the given string to the
    script output.

    """
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """Run migrations in 'online' mode.

    In this scenario we need to create an Engine
    and associate a connection with the context.

    """
    connectable = engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection, target_metadata=target_metadata
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
