import httpx

from fastid.settings import settings


async def test_get(client: httpx.AsyncClient, db_migrations):
    response = await client.get(url='/api/v1/config/')
    assert response.status_code == httpx.codes.OK
    assert response.json().get('jwt_iss') == settings.jwt_iss
