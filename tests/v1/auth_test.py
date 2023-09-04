import httpx
from pytest_mock import MockerFixture

from fastid.exceptions import RecaptchaVerifyFailException


async def test_users_create(client: httpx.AsyncClient, db_migrations, mock_aiosmtplib):
    response = await client.post(
        url='/api/v1/auth/email/',
        json={
            'email': 'user@example.com',
            'password': 'password',
            'recaptcha_verify': 'recaptcha_verify',
        },
    )
    assert response.status_code == httpx.codes.CREATED
    assert response.json().get('confirmation_token')


async def test_users_create_by_email_fail(client: httpx.AsyncClient, mocker: MockerFixture):
    mocker.patch('fastid.services.recaptcha.check_verify', side_effect=RecaptchaVerifyFailException())

    response = await client.post(
        url='/api/v1/auth/email/',
        json={
            'email': 'user@example.com',
            'password': 'password',
            'recaptcha_verify': 'recaptcha_verify',
        },
    )
    assert response.status_code == httpx.codes.BAD_REQUEST
    assert response.json() == {'error': 'Recaptcha verify fail'}


async def test_users_create_empty_email(client: httpx.AsyncClient):
    response = await client.post(
        url='/api/v1/auth/email/',
        json={
            'password': 'password',
            'recaptcha_verify': 'recaptcha_verify',
        },
    )
    assert response.status_code == httpx.codes.UNPROCESSABLE_ENTITY


async def test_users_create_empty_recaptcha(client: httpx.AsyncClient):
    response = await client.post(
        url='/api/v1/auth/email/',
        json={
            'password': 'password',
        },
    )
    assert response.status_code == httpx.codes.UNPROCESSABLE_ENTITY


async def test_users_create_by_email_exception(client: httpx.AsyncClient, mocker: MockerFixture):
    mocker.patch('fastid.services.recaptcha.check_verify', side_effect=Exception())

    response = await client.post(
        url='/api/v1/auth/email/',
        json={
            'email': 'user@example.com',
            'password': 'password',
            'recaptcha_verify': 'recaptcha_verify',
        },
    )
    assert response.status_code == httpx.codes.INTERNAL_SERVER_ERROR
    assert response.json() == {'error': 'Internal server error'}
