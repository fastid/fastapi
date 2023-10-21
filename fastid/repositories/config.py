from typing import Sequence

from sqlalchemy import delete, insert, select

from ..trace import decorator_trace
from . import db, schemes


@decorator_trace(name='repositories.config.get')
async def get() -> Sequence[schemes.Config] | None:
    async with db.async_session() as session:
        stmt = select(schemes.Config)
        session_obj = await session.scalars(stmt)
        return session_obj.all()


@decorator_trace(name='repositories.config.update')
async def update(*, key: str, value: str | list[str]) -> list[schemes.Config] | None:
    async with db.async_session() as session:
        stmt = delete(schemes.Config).where(schemes.Config.key == key)
        await session.execute(stmt)

        value_data = []
        if isinstance(value, str):
            value_data.append({'key': key, 'value': value})
        else:
            for item in value:
                value_data.append({'key': key, 'value': item})

        stmt_insert = insert(schemes.Config).values(value_data)
        await session.execute(stmt_insert)
        await session.commit()
    return await get()
