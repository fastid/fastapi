import httpx


async def test_info(client_auth: httpx.AsyncClient):
    response = await client_auth.get(url='/api/v1/users/info/')
    assert response.status_code == httpx.codes.OK
    assert response.json().get('created_at')
    assert response.json().get('updated_at')
    assert response.json().get('email') == 'user@exmaple.com'
    assert response.json().get('user_id')

    assert response.json().get('profile').get('language') == 'en'
    assert response.json().get('profile').get('timezone') == 'UTC'
    assert response.json().get('profile').get('locate') == 'en-us'


async def test_invalid_token(client: httpx.AsyncClient):
    response = await client.get(url='/api/v1/users/info/')
    assert response.status_code == httpx.codes.UNAUTHORIZED


async def test_invalid_fake_token(client: httpx.AsyncClient):
    response = await client.get(url='/api/v1/users/info/', headers={'Authorization': 'Bearer fake'})
    assert response.status_code == httpx.codes.UNAUTHORIZED
