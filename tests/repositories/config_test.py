from sqlalchemy import insert

from fastid import repositories


async def test_get(db_migrations):
    async with repositories.db.async_session() as session:
        stmt = insert(repositories.schemes.Config).values(key='is_setup', value='1')
        await session.execute(stmt)
        await session.commit()

    config = await repositories.config.get()
    assert config[0].key == 'is_setup'
    assert config[0].value == '1'


async def test_get_empty(db_migrations):
    config = await repositories.config.get()
    assert config == []


async def test_update(db_migrations):
    config1 = await repositories.config.update(key='test', value=['val1', 'val2'])

    assert config1[0].key == 'test'
    assert config1[0].value == 'val1'

    assert config1[1].key == 'test'
    assert config1[1].value == 'val2'

    config2 = await repositories.config.update(key='test', value='val')
    assert config2[0].key == 'test'
    assert config2[0].value == 'val'
