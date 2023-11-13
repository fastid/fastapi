from fastid import services


async def test_get(db_migrations):
    for language in await services.language.get_all():
        if language.value == 'en-us':
            assert language.name == 'English (United States)'
