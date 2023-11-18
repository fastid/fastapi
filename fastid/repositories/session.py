import hashlib
import uuid
from datetime import datetime
from typing import Union
from zoneinfo import ZoneInfo

from sqlalchemy import delete, insert, select

from .. import repositories, typing
from ..trace import decorator_trace
from . import db, schemes


@decorator_trace(name='repositories.session.create')
async def create(
    *,
    expires_at: datetime,
    data: dict[str, Union[bool, str, int]] | None = None,
) -> schemes.Sessions | None:
    m = hashlib.sha256()
    m.update(str(uuid.uuid4()).encode('utf-8'))

    stmt = (
        insert(schemes.Sessions)
        .values(
            expires_at=expires_at,
            session_key=m.hexdigest(),
            data=data if data else {},
        )
        .returning(schemes.Sessions)
    )

    async with repositories.db.async_session() as session:
        result = await session.execute(stmt)
        await session.commit()
        return result.scalar()


@decorator_trace(name='repositories.session.get_by_id')
async def get_by_id(*, session_id: typing.SessionID) -> schemes.Sessions | None:
    stmt = select(schemes.Sessions).where(
        schemes.Sessions.session_id == session_id,
        schemes.Sessions.expires_at >= datetime.now(tz=ZoneInfo('UTC')),
    )

    async with db.async_session() as session:
        return await session.scalar(stmt)


@decorator_trace(name='repositories.session.get_by_session_key')
async def get_by_session_key(*, session_key: str) -> schemes.Sessions | None:
    stmt = select(schemes.Sessions).where(
        schemes.Sessions.session_key == session_key,
        schemes.Sessions.expires_at >= datetime.now(tz=ZoneInfo('UTC')),
    )
    async with db.async_session() as session:
        return await session.scalar(stmt)


@decorator_trace(name='repositories.session.delete_by_id')
async def delete_by_id(*, session_id: typing.SessionID) -> bool:
    stmt = delete(schemes.Sessions).where(
        schemes.Sessions.session_id == session_id,
        schemes.Sessions.expires_at >= datetime.now(tz=ZoneInfo('UTC')),
    )

    async with db.async_session() as session:
        result = await session.execute(stmt)
        await session.commit()

        if result.rowcount:
            return True
        return False
