from datetime import datetime
from typing import Union
from uuid import UUID

from sqlalchemy import delete, select

from ..exceptions import NotFoundException
from . import db, schemes


async def create(
    *,
    session_id: UUID,
    expire_at: datetime,
    data: dict[str, Union[bool, str, int]] | None = None,
) -> schemes.Sessions:
    session_obj = schemes.Sessions(
        session_id=session_id,
        expire_at=expire_at,
        data=data if data else {},
    )

    async with db.async_session() as session:
        await session.begin()
        session.add(session_obj)
        await session.commit()

    return session_obj


async def get(*, session_id: UUID) -> schemes.Sessions | None:
    async with db.async_session() as session:
        stmt = select(schemes.Sessions).where(schemes.Sessions.session_id == session_id)
        session_obj = await session.scalar(stmt)
        if session_obj is None:
            raise NotFoundException(message='session not found')

        return session_obj


async def remove(*, session_id: UUID) -> None:
    async with db.async_session() as session:
        stmt = delete(schemes.Sessions).where(schemes.Sessions.session_id == session_id)
        await session.execute(stmt)
        await session.commit()
