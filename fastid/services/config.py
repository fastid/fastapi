from ..settings import settings
from ..trace import decorator_trace
from . import models


@decorator_trace(name='services.config.get')
async def get() -> models.Config:
    print(settings.captcha)

    return models.Config(
        captcha=settings.captcha,
        captcha_usage=settings.captcha_usage.split(',') if settings.captcha_usage else [],
        recaptcha_site_key=settings.recaptcha_site_key,
        jwt_iss=settings.jwt_iss,
        password_policy_min_length=settings.password_policy_min_length,
        password_policy_max_length=settings.password_policy_max_length,
    )

    # captcha_usage = []
    # for obj in config_repo:
    #     if obj.key == 'is_setup':
    #         config.is_setup = True
    #     elif obj.key == 'captcha':
    #         config.captcha = obj.value
    #     elif obj.key == 'recaptcha_site_key':
    #         config.recaptcha_site_key = obj.value
    #     elif obj.key == 'captcha_usage':
    #         captcha_usage.append(obj.value)

    # if captcha_usage:
    #     config.captcha_usage = captcha_usage
