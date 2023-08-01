from sqlalchemy import text

from fastid import repositories


async def test_engine():
    async with repositories.db.async_session() as session:
        async with session.begin():
            result = await session.execute(text('select 1'))
            assert result.scalar_one_or_none() == 1
