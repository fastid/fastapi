import pytest

from fastid import repositories, services, typing
from fastid.exceptions import NotFoundException


async def test_create(db_migrations):
    user_id = await repositories.users.create(
        email=typing.Email('user@example.com'),
        password=typing.Password('password'),
    )

    jwt_token = await services.tokens.create(audience='test_audience', user_id=user_id)
    assert jwt_token.access_token
    assert jwt_token.refresh_token
    assert jwt_token.token_type
    assert jwt_token.expires_in


async def test_update(db_migrations):
    user_id = await repositories.users.create(
        email=typing.Email('user@example.com'),
        password=typing.Password('password'),
    )

    jwt_token = await services.tokens.create(audience='test_audience', user_id=user_id)
    token = await services.tokens.update(refresh_token=jwt_token.refresh_token, audience='test_audience')
    assert token.access_token
    assert token.refresh_token
    assert token.token_type
    assert token.expires_in


async def test_update_exception(db_migrations):
    with pytest.raises(NotFoundException):
        await services.tokens.update(refresh_token='fake_token', audience='test_audience')
