import httpx


async def test_healthcheck(client: httpx.AsyncClient):
    response = await client.get(url='/healthcheck/')
    assert response.status_code == httpx.codes.OK


async def test_raise_error(client: httpx.AsyncClient):
    response = await client.get(url='/healthcheck/?raise_error=true')
    assert response.status_code == httpx.codes.INTERNAL_SERVER_ERROR
