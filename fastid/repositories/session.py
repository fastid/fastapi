from datetime import datetime
from typing import Union
from uuid import UUID

from sqlalchemy import delete, insert, select

from .. import repositories, typing
from ..exceptions import NotFoundException
from ..trace import decorator_trace
from . import db, schemes


@decorator_trace(name='repositories.session.create')
async def create(
    *,
    session_id: typing.SessionID,
    expires_at: datetime,
    data: dict[str, Union[bool, str, int]] | None = None,
) -> schemes.Sessions:
    stmt = insert(schemes.Sessions).values(
        session_id=session_id,
        expires_at=expires_at,
        data=data if data else {},
    )

    async with repositories.db.async_session() as session:
        await session.execute(stmt)
        await session.commit()

    return await get(session_id=session_id)


@decorator_trace(name='repositories.session.get')
async def get(*, session_id: UUID) -> schemes.Sessions | None:
    stmt = select(schemes.Sessions).where(schemes.Sessions.session_id == session_id)

    async with db.async_session() as session:
        session_obj = await session.scalar(stmt)
        if session_obj is None:
            raise NotFoundException(message='session not found')

        return session_obj


@decorator_trace(name='repositories.session.delete_by_id')
async def delete_by_id(*, session_id: UUID) -> bool:
    stmt = delete(schemes.Sessions).where(schemes.Sessions.session_id == session_id)

    async with db.async_session() as session:
        result = await session.execute(stmt)
        await session.commit()

        if result.rowcount:
            return True
        return False
