import httpx


async def test_static(client: httpx.AsyncClient):
    response = await client.get(url='/')
    assert response.status_code == httpx.codes.OK


async def test_static_signin(client: httpx.AsyncClient):
    response = await client.get(url='/signin/')
    assert response.status_code == httpx.codes.OK


async def test_static_settings_not_found(client: httpx.AsyncClient):
    response = await client.get(url='/api/v1/settings_not_found/')
    assert response.status_code == httpx.codes.NOT_FOUND
