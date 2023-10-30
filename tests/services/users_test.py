import pytest

from fastid import services, typing
from fastid.exceptions import NotFoundException


async def test_create(db_migrations):
    user_id = await services.users.create(
        email=typing.Email('user@exmaple.com'),
        password=typing.Password('password'),
    )
    assert user_id


async def test_get_by_email(db_migrations):
    user_id = await services.users.create(
        email=typing.Email('user@exmaple.com'),
        password=typing.Password('password'),
    )
    assert user_id

    user = await services.users.get_by_email(email=typing.Email('user@exmaple.com'))
    assert user.email == typing.Email('user@exmaple.com')
    assert user.user_id == 1
    assert user.password


async def test_get_by_email_not_found(db_migrations):
    user = await services.users.get_by_email(email=typing.Email('user@exmaple.com'))
    assert user is None


async def test_signin(db_migrations):
    await services.users.create(
        email=typing.Email('user@exmaple.com'),
        password=typing.Password('password'),
    )
    token = await services.users.signin(email=typing.Email('user@exmaple.com'))
    assert token.refresh_token
    assert token.access_token
    assert token.token_type


async def test_exception(db_migrations):
    with pytest.raises(NotFoundException):
        await services.users.signin(email=typing.Email('user@exmaple.com'))
