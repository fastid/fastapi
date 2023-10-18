import pytest

from fastid import services, typing
from fastid.exceptions import BadRequestException


async def test_create_user(db_migrations):
    token = await services.admin.create_user(
        email=typing.Email('user@exmaple.com'),
        password=typing.Password('password'),
    )
    assert token.access_token
    assert token.refresh_token


# Checking that the project is activated
async def test_create_user_project_is_setup(db_migrations):
    await services.config.update('is_setup', 'True')

    with pytest.raises(BadRequestException):
        await services.admin.create_user(
            email=typing.Email('user@exmaple.com'),
            password=typing.Password('password'),
        )
