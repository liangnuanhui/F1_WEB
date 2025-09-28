from logging.config import fileConfig

from sqlalchemy import engine_from_config
from sqlalchemy import pool

from alembic import context

# 导入我们的模型 - 确保所有模型都被导入以进行正确的迁移
from app.models.base import Base
from app.models.season import Season
from app.models.circuit import Circuit
from app.models.race import Race
from app.models.driver import Driver
from app.models.constructor import Constructor
from app.models.result import Result
from app.models.driver_season import DriverSeason
from app.models.qualifying_result import QualifyingResult
from app.models.sprint_result import SprintResult
from app.models.standings import DriverStanding, ConstructorStanding

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


def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode.

    This configures the context with just a URL
    and not an Engine, though an Engine is acceptable
    here as well.  By skipping the Engine creation
    we don't even need a DBAPI to be available.

    Calls to context.execute() here emit the given string to the
    script output.

    """
    # 优先使用环境变量中的数据库URL
    import os
    url = os.getenv("DATABASE_URL") or config.get_main_option("sqlalchemy.url")
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
    # 使用环境变量中的数据库URL
    import os
    database_url = os.getenv("DATABASE_URL")

    if database_url:
        # 如果有环境变量，直接使用
        from sqlalchemy import create_engine
        connectable = create_engine(database_url)
    else:
        # 否则使用配置文件
        configuration = config.get_section(config.config_ini_section)
        configuration = configuration or {}

        # 确保有数据库URL
        if 'sqlalchemy.url' not in configuration:
            raise ValueError("No database URL found in environment variable DATABASE_URL or alembic.ini")

        connectable = engine_from_config(
            configuration,
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
