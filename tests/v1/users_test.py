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


async def test_language(client_auth: httpx.AsyncClient):
    response = await client_auth.get(url='/api/v1/users/language/')
    assert response.status_code == httpx.codes.OK
    assert isinstance(response.json().get('results'), list)
    assert response.json().get('results')[0].get('name') == 'English (United States)'
    assert response.json().get('results')[0].get('value') == 'en-us'


async def test_timezone(client_auth: httpx.AsyncClient):
    response = await client_auth.get(url='/api/v1/users/timezone/')
    assert response.status_code == httpx.codes.OK
    assert isinstance(response.json().get('results'), list)


async def test_change_locate(client_auth: httpx.AsyncClient):
    response = await client_auth.post(url='/api/v1/users/language/', json={'locate': 'en-gb'})
    assert response.status_code == httpx.codes.OK

    response = await client_auth.get(url='/api/v1/users/info/')
    assert response.json().get('profile').get('language') == 'en'
    assert response.json().get('profile').get('locate') == 'en-gb'


async def test_change_locate_not_found(client_auth: httpx.AsyncClient):
    response = await client_auth.post(url='/api/v1/users/language/', json={'locate': 'fk-fk'})
    assert response.status_code == httpx.codes.NOT_FOUND
