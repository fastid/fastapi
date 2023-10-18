import datetime
import uuid
from datetime import timedelta
from zoneinfo import ZoneInfo

import pytest

from fastid import repositories, typing
from fastid.exceptions import NotFoundException


async def test_create(db_migrations):
    session = await repositories.session.create(
        session_id=typing.SessionID(uuid.uuid4()),
        expires_at=datetime.datetime.now(tz=ZoneInfo('UTC')) + timedelta(days=1),
    )
    assert session.session_id
    assert session.expires_at


async def test_not_found(db_migrations):
    with pytest.raises(NotFoundException):
        await repositories.session.get(session_id=typing.SessionID(uuid.uuid4()))


async def test_delete(db_migrations):
    session = await repositories.session.create(
        session_id=typing.SessionID(uuid.uuid4()),
        expires_at=datetime.datetime.now(tz=ZoneInfo('UTC')) + timedelta(days=1),
    )
    result = await repositories.session.delete_by_id(session_id=typing.SessionID(session.session_id))
    assert result

    result_not_found = await repositories.session.delete_by_id(session_id=typing.SessionID(uuid.uuid4()))
    assert not result_not_found
