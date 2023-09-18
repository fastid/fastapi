from urllib.parse import parse_qs, urlparse

import httpx

from fastid import repositories


async def test_authorize_code(client: httpx.AsyncClient, db_migrations):
    client_id = await repositories.applications.create(
        name='Test application',
        redirect_uri=[
            'http://localhost/',
            'http://localhost.localhost/',
        ],
    )

    response = await client.get(
        url='/oauth/authorize/',
        params={
            'client_id': client_id,
            'response_type': 'code',
            'redirect_uri': 'http://localhost/',
            'state': 'test_state',
        },
    )
    assert response.status_code == httpx.codes.TEMPORARY_REDIRECT
    assert response.headers.get('location')

    qs = urlparse(response.headers.get('location')).query
    assert qs

    assert parse_qs(qs).get('state')[0] == 'test_state'
    assert parse_qs(qs).get('code')[0]


async def test_authorize_code_not_found_redirect_uri(client: httpx.AsyncClient, db_migrations):
    client_id = await repositories.applications.create(
        name='Test application',
        redirect_uri=[
            'http://localhost/',
            'http://localhost.localhost/',
        ],
    )

    response = await client.get(
        url='/oauth/authorize/',
        params={
            'client_id': client_id,
            'response_type': 'code',
            'redirect_uri': 'https://localhost/',
            'state': 'test_state',
        },
    )
    assert response.status_code == httpx.codes.BAD_REQUEST


async def test_authorize_token(client: httpx.AsyncClient, db_migrations):
    client_id = await repositories.applications.create(
        name='Test application',
        redirect_uri=[
            'http://localhost/',
            'http://localhost.localhost/',
        ],
    )

    response = await client.get(
        url='/oauth/authorize/',
        params={
            'client_id': client_id,
            'response_type': 'token',
            'redirect_uri': 'http://localhost/',
            'state': 'test_state',
        },
    )
    assert response.status_code == httpx.codes.TEMPORARY_REDIRECT
    assert response.headers.get('location')

    qs = urlparse(response.headers.get('location')).fragment
    assert parse_qs(qs).get('access_token')[0]
    assert parse_qs(qs).get('token_type')[0] == 'Bearer'
    assert parse_qs(qs).get('expires_in')[0]
    assert parse_qs(qs).get('state')[0] == 'test_state'
