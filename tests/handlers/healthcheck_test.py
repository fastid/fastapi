import httpx


async def test_healthcheck(client: httpx.AsyncClient):
    response = await client.get(url='/healthcheck/')
    assert response.status_code == httpx.codes.OK
