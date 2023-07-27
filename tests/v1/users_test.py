import httpx
from pytest_httpx import HTTPXMock

from fastid.exceptions import RecaptchaVerifyFailException


async def test_users_create(client: httpx.AsyncClient):
    response = await client.post(
        url='/api/v1/users/email/',
        json={
            'email': 'user@example.com',
            'password': 'password',
            'recaptcha_verify': 'recaptcha_verify',
        },
    )
    assert response.status_code == 201


async def test_users_create_by_email_fail(client: httpx.AsyncClient, mocker):
    with mocker.patch('fastid.services.recaptcha.check_verify', side_effect=RecaptchaVerifyFailException()):
        response = await client.post(
            url='/api/v1/users/email/',
            json={
                'email': 'user@example.com',
                'password': 'password',
                'recaptcha_verify': 'recaptcha_verify',
            },
        )
        assert response.status_code == 400
        assert response.json() == {'error': 'Recaptcha verify fail'}
