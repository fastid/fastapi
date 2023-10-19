import httpx


async def test_updates_refresh_token(client: httpx.AsyncClient, db_migrations):
    response = await client.post(
        url='/api/v1/admin/signup/',
        json={
            'email': 'user@exmaple.com',
            'password': 'password',
        },
    )

    assert response.status_code == httpx.codes.CREATED
    assert response.json().get('access_token')
    assert response.json().get('refresh_token')
    assert response.json().get('expires_in')
    assert response.json().get('token_type')

    response = await client.post(
        url='/api/v1/users/refresh_token/',
        json={
            'refresh_token': response.json().get('access_token'),
        },
    )
    assert response.status_code == httpx.codes.OK
    assert response.json().get('access_token')
    assert response.json().get('refresh_token')
    assert response.json().get('expires_in')
    assert response.json().get('token_type')
