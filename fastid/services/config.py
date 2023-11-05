from ..settings import settings
from ..trace import decorator_trace
from . import models


@decorator_trace(name='services.config.get')
async def get() -> models.Config:
    return models.Config(
        captcha=settings.captcha,
        captcha_usage=settings.captcha_usage.split(',') if settings.captcha_usage else [],
        recaptcha_site_key=settings.recaptcha_site_key,
        jwt_iss=settings.jwt_iss,
        password_policy_min_length=settings.password_policy_min_length,
        password_policy_max_length=settings.password_policy_max_length,
        link_github=settings.link_github,
        logo_url=settings.logo_url,
        logo_title=settings.logo_title,
    )
