from datetime import datetime, timedelta
from typing import Union
from zoneinfo import ZoneInfo

from .. import repositories, typing
from ..trace import decorator_trace
from . import models


@decorator_trace(name='services.session.create')
async def create(
    expire_time_second: int = 60 * 60 * 24,
    data: dict[str, Union[bool, str, int]] | None = None,
) -> models.Session:
    expires_at = datetime.now(tz=ZoneInfo('UTC')) + timedelta(seconds=expire_time_second)

    # We write it to the database
    session = await repositories.session.create(expires_at=expires_at, data=data)
    return models.Session.model_validate(session)


@decorator_trace(name='services.session.get_by_id')
async def get_by_id(*, session_id: typing.SessionID) -> models.Session:
    session = await repositories.session.get_by_id(session_id=session_id)
    return models.Session.model_validate(session)


@decorator_trace(name='services.session.get_by_session_key')
async def get_by_session_key(*, session_key: str) -> models.Session | None:
    session = await repositories.session.get_by_session_key(session_key=session_key)
    if session is None:
        return None
    return models.Session.model_validate(session)


@decorator_trace(name='services.session.delete_by_id')
async def delete_by_id(*, session_id: typing.SessionID) -> bool:
    return await repositories.session.delete_by_id(session_id=session_id)
