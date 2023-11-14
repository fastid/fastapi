from fastid import services


async def test_get_all():
    timezone = await services.timezone.get_all()
    for tz in timezone:
        if tz.timezone == 'America/Los_Angeles':
            assert tz.ru == 'Сан-Франциско, Лос-Анджелес, Сан-Диего'
            assert tz.en == 'San Francisco, Los Angeles, San Diego'
