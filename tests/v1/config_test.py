import httpx

from fastid.settings import settings


async def test_get(client: httpx.AsyncClient, db_migrations):
    response = await client.get(url='/api/v1/config/')
    assert response.status_code == httpx.codes.OK

    assert not response.json().get('is_setup')
    assert response.json().get('captcha') is None
    assert response.json().get('recaptcha_site_key') is None
    assert response.json().get('captcha_usage') == []
    assert response.json().get('jwt_iss') == settings.jwt_iss
