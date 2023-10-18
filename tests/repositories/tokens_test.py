import datetime
import uuid
from datetime import timedelta
from zoneinfo import ZoneInfo

import pytest

from fastid import repositories, typing
from fastid.exceptions import NotFoundException


async def test_create(db_migrations):
    user_id = await repositories.users.create(
        email=typing.Email('user@exmaple.com'),
        password=typing.Password('Password'),
    )

    token_id = await repositories.tokens.create(
        token_id=typing.TokenID(uuid.uuid4()),
        access_token='access_token',
        refresh_token='refresh_token',
        user_id=user_id,
        expires_at=datetime.datetime.now(tz=ZoneInfo('UTC')) + timedelta(days=1),
    )
    assert token_id


async def test_get_by_id(db_migrations):
    user_id = await repositories.users.create(
        email=typing.Email('user@exmaple.com'),
        password=typing.Password('Password'),
    )

    token_id = await repositories.tokens.create(
        token_id=typing.TokenID(uuid.uuid4()),
        access_token='access_token',
        refresh_token='refresh_token',
        user_id=user_id,
        expires_at=datetime.datetime.now(tz=ZoneInfo('UTC')) + timedelta(days=1),
    )
    token = await repositories.tokens.get_by_id(token_id=token_id)
    assert token.token_id == token_id
    assert token.access_token == 'access_token'
    assert token.refresh_token == 'refresh_token'
    assert token.user_id == user_id
    assert token.expires_at


async def test_get_by_id_mot_found(db_migrations):
    with pytest.raises(NotFoundException):
        await repositories.tokens.get_by_id(token_id=typing.TokenID(uuid.uuid4()))


async def test_delete_by_id(db_migrations):
    user_id = await repositories.users.create(
        email=typing.Email('user@exmaple.com'),
        password=typing.Password('Password'),
    )

    token_id = await repositories.tokens.create(
        token_id=typing.TokenID(uuid.uuid4()),
        access_token='access_token',
        refresh_token='refresh_token',
        user_id=user_id,
        expires_at=datetime.datetime.now(tz=ZoneInfo('UTC')) + timedelta(days=1),
    )
    token_is_delete = await repositories.tokens.delete_by_id(token_id=token_id)
    assert token_is_delete

    token_is_delete_not_found = await repositories.tokens.delete_by_id(token_id=typing.TokenID(uuid.uuid4()))
    assert not token_is_delete_not_found
