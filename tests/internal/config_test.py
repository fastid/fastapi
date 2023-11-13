import httpx

from fastid.settings import settings


async def test_get(client: httpx.AsyncClient, db_migrations):
    response = await client.get(url='/api/v1/internal/config/')
    assert response.status_code == httpx.codes.OK
    assert response.json().get('jwt_iss') == settings.jwt_iss
    assert response.json().get('recaptcha_site_key')
    assert response.json().get('password_policy_max_length')
    assert response.json().get('password_policy_min_length')
    assert response.json().get('captcha')
