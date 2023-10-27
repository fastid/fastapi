from fastid.redis_client import redis_client


async def test_get_set(mock_redis_client):
    async with redis_client() as client:
        assert await client.set('hello', 'word')
        assert await client.get('hello') == 'word'


async def test_not_found(mock_redis_client):
    async with redis_client() as client:
        assert not await client.get('not_found')


async def test_python_object(mock_redis_client):
    async with redis_client() as client:
        await client.hset('counter', 'users', 20)
        await client.expire(name='counter', time=100)

        assert await client.hget('counter', 'users') == '20'
        assert await client.hdel('counter', 'users') == 1
