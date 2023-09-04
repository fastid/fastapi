from fastid import repositories


async def test_create(db_migrations):
    client_id = await repositories.applications.create(
        name='Test application',
        redirect_uri=['https://yandex.ru/'],
    )
    assert client_id


async def test_get(db_migrations):
    client_id = await repositories.applications.create(
        name='Test application',
        redirect_uri=['   https://yandex.RU/   '],
    )

    assert client_id

    application = await repositories.applications.get_by_client_id(client_id=client_id)

    for uri in application.redirect_uri:
        assert uri.uri == 'https://yandex.ru/'
        break
