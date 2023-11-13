import uuid
from datetime import datetime, timedelta
from typing import AsyncGenerator
from zoneinfo import ZoneInfo

import pytest

from fastid import repositories, typing
from fastid.repositories import schemes


@pytest.fixture
async def user(db_migrations) -> AsyncGenerator[schemes.Users, None]:
    user = await repositories.users.create(
        email=typing.Email('user@exmaple.com'),
        password=typing.Password('qwerty'),
    )
    assert isinstance(user, repositories.schemes.Users)

    assert user is not None
    assert user.user_id
    assert user.email == typing.Email('user@exmaple.com')
    assert user.password == typing.Password('qwerty')
    assert user.created_at
    assert user.updated_at
    assert user.deleted_at is None

    assert user.profile.profile_id
    assert user.profile.created_at
    assert user.profile.updated_at
    assert user.profile.deleted_at is None
    assert user.profile.language == typing.Language.EN
    assert user.profile.locate == typing.Locate.EN_US
    assert user.profile.timezone == 'UTC'

    yield user


@pytest.fixture
async def token(user: schemes.Users) -> AsyncGenerator[schemes.Tokens, None]:
    token = await repositories.tokens.create(
        token_id=typing.TokenID(uuid.uuid4()),
        access_token='access_token',
        refresh_token='refresh_token',
        user_id=user.user_id,
        expires_at=datetime.now(tz=ZoneInfo('UTC')) + timedelta(days=1),
    )
    assert token
    assert isinstance(token, repositories.schemes.Tokens)
    assert token.token_id
    assert token.access_token == 'access_token'
    assert token.refresh_token == 'refresh_token'
    assert token.user_id
    assert token.expires_at
    assert token.created_at
    assert token.updated_at

    yield token
