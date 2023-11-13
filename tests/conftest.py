from typing import AsyncGenerator

import httpx
import pytest
from asgi_lifespan import LifespanManager
from fastapi import FastAPI
from pytest_mock import MockerFixture

from fastid import repositories, services, typing
from fastid.app import app as application


@pytest.fixture()
async def app() -> AsyncGenerator[FastAPI, None]:
    async with LifespanManager(application):
        yield application


@pytest.fixture()
async def db_migrations() -> AsyncGenerator[None, None]:
    """
    Fixture for migrations db

    :return: AsyncGenerator
    """
    async with repositories.db.engine.begin() as conn:
        await conn.run_sync(repositories.schemes.Base.metadata.create_all)
        yield
        await conn.run_sync(repositories.schemes.Base.metadata.drop_all)


@pytest.fixture
async def mock_aiosmtplib(mocker: MockerFixture):
    mocker.patch('aiosmtplib.SMTP.connect', return_value='220 connect smtp server')
    mocker.patch('aiosmtplib.SMTP.sendmail', return_value=(None, '2.0.0 Ok: queued'))
    mocker.patch('aiosmtplib.SMTP.quit', return_value='221 2.0.0 Closing connection')


@pytest.fixture()
async def client(app: FastAPI) -> AsyncGenerator[httpx.AsyncClient, None]:
    headers = {'x-real-ip': '127.0.0.1'}

    async with httpx.AsyncClient(app=app, base_url='http://localhost.local', headers=headers) as client:
        try:
            yield client
        finally:
            await client.aclose()


@pytest.fixture()
async def client_internal_auth(app: FastAPI, db_migrations) -> AsyncGenerator[httpx.AsyncClient, None]:
    user = await services.users.create(
        email=typing.Email('user@exmaple.com'),
        password=typing.Password('qwerty'),
    )
    token = await services.tokens.create(audience='internal', user_id=user.user_id)
    headers = {
        'x-real-ip': '127.0.0.1',
        'Authorization': f'Bearer {token.access_token}',
    }

    async with httpx.AsyncClient(app=app, base_url='http://localhost.local', headers=headers) as client:
        try:
            yield client
        finally:
            await client.aclose()
