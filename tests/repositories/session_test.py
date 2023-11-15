import datetime
from datetime import timedelta
from typing import AsyncGenerator
from zoneinfo import ZoneInfo

import pytest

from fastid import repositories, typing
from fastid.repositories import schemes


@pytest.fixture
async def session(db_migrations) -> AsyncGenerator[schemes.Sessions, None]:
    session = await repositories.session.create(
        expires_at=datetime.datetime.now(tz=ZoneInfo('UTC')) + timedelta(days=1),
        data={'hello': 'word'},
    )
    assert len(session.session_key) == 64
    assert session.session_id
    assert session.expires_at
    assert session.data.get('hello') == 'word'
    yield session


async def test_get_by_id(session: schemes.Sessions):
    session = await repositories.session.get_by_id(session_id=session.session_id)
    assert len(session.session_key) == 64
    assert session.session_id
    assert session.expires_at
    assert session.data.get('hello') == 'word'


async def test_get_by_session_key(session: schemes.Sessions):
    session = await repositories.session.get_by_session_key(session_key=session.session_key)
    assert len(session.session_key) == 64
    assert session.session_id
    assert session.expires_at
    assert session.data.get('hello') == 'word'


async def test_delete_by_id(session: schemes.Sessions):
    result = await repositories.session.delete_by_id(session_id=session.session_id)
    assert result

    result_not_found = await repositories.session.delete_by_id(session_id=typing.SessionID(999))
    assert not result_not_found
