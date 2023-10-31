from fastid import services


async def test_get(db_migrations):
    config = await services.config.get()
    assert config.recaptcha_site_key
    assert config.jwt_iss
    assert config.password_policy_max_length
    assert config.password_policy_min_length
