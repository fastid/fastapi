from typing import AsyncGenerator

import pytest

from fastid import services
from fastid.services import models


@pytest.fixture
async def session(db_migrations) -> AsyncGenerator[models.Session, None]:
    session_obj = await services.session.create(expire_time_second=60 * 60 * 24)
    assert isinstance(session_obj, models.Session)
    assert session_obj.session_id
    assert session_obj.session_key
    assert session_obj.expires_at
    yield session_obj


async def test_get_by_id(session: models.Session):
    session = await services.session.get_by_id(session_id=session.session_id)
    assert isinstance(session, models.Session)
    assert session.session_id
    assert session.session_key
    assert session.expires_at


async def test_get_by_session_key(session: models.Session):
    session = await services.session.get_by_session_key(session_key=session.session_key)
    assert isinstance(session, models.Session)
    assert session.session_id
    assert session.session_key
    assert session.expires_at


async def test_delete_by_id(session: models.Session):
    result = await services.session.delete_by_id(session_id=session.session_id)
    assert result
