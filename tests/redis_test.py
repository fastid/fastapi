from fastid.redis_client import redis_client


async def test_get_set(mock_redis_client):
    async with redis_client() as client:
        await client.set('hello', 'word')
        assert await client.get('hello') == 'word'


async def test_not_found(mock_redis_client):
    async with redis_client() as client:
        assert not await client.get('not_found')
