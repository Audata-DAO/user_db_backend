import asyncio
from logging.config import fileConfig

from alembic import context
from sqlalchemy import pool
from sqlalchemy.ext.asyncio import create_async_engine

from app.core.config import settings

config = context.config


if config.config_file_name is not None:
    fileConfig(config.config_file_name)

from app.core.models import SQLModel # noqa: F401, E402

target_metadata = SQLModel.metadata


def get_url():
    return str(settings.DATABASE_URL)


def run_migrations_offline() -> None:
    url = get_url()

    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    configuration = config.get_section(config.config_ini_section)
    configuration["sqlalchemy.url"] = get_url()

    connectable = create_async_engine(
        configuration["sqlalchemy.url"],
        poolclass=pool.NullPool,
    )

    async def do_run_migrations(connection):
        def do_upgrades(connection_):
            context.configure(
                connection=connection_,
                target_metadata=target_metadata,
            )
            try:
                with context.begin_transaction():
                    context.run_migrations()
            except Exception as e:
                print(f"Error during migration: {e}")
                connection_.rollback()
                raise

        await connection.run_sync(do_upgrades)

    async def run_async_migrations():
        async with connectable.connect() as connection:
            await do_run_migrations(connection)
        await connectable.dispose()

    asyncio.run(run_async_migrations())


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
