import os

from sqlalchemy import URL
from sqlalchemy.ext.asyncio import AsyncEngine, async_sessionmaker, create_async_engine

from fastid.settings import Environment

from ..settings import settings


def _get_engine() -> AsyncEngine:
    _engine = create_async_engine(
        url=URL.create(
            drivername='postgresql+asyncpg',
            username=settings.db_user,
            password=settings.db_password.get_secret_value(),
            host=settings.db_host,
            port=settings.db_port,
            database=settings.db_database,
        ),
        echo=True,
        pool_size=settings.db_pool_size,
        max_overflow=settings.db_max_overflow,
        connect_args={
            'server_settings': {
                'application_name': settings.app_name,
                'search_path': settings.db_schema,
            },
        },
        hide_parameters=True if settings.environment == Environment.production else False,
    )

    if os.getenv('PYTEST'):
        _engine = create_async_engine('sqlite+aiosqlite:///:memory:')

    return _engine


engine = _get_engine()

async_session = async_sessionmaker(
    engine,
    expire_on_commit=False,
    autocommit=False,
    autoflush=False,
    future=True,
)
