from fastid import services


async def test_get(db_migrations):
    await services.config.update(key='is_setup', value='1')
    await services.config.update(key='captcha', value='recaptcha')
    await services.config.update(key='recaptcha_site_key', value='12345')
    await services.config.update(key='captcha_usage', value='signin')
    await services.config.update(key='password_policy_min_length', value='6')
    await services.config.update(key='password_policy_max_length', value='200')

    config = await services.config.get()
    assert config.is_setup == True
    assert config.captcha == 'recaptcha'
    assert config.captcha_usage == ['signin']
    assert config.recaptcha_site_key == '12345'
    assert config.jwt_iss == 'FastID'
