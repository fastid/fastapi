from .. import repositories
from ..settings import settings
from . import models


async def get() -> models.Config:
    config_repo = await repositories.config.get()

    config = models.Config(
        is_setup=False,
        captcha=None,
        captcha_usage=[],
        recaptcha_site_key=None,
        jwt_iss=settings.jwt_iss,
    )

    captcha_usage = []
    for obj in config_repo:
        if obj.key == 'is_setup':
            config.is_setup = True
        elif obj.key == 'captcha':
            config.captcha = obj.value
        elif obj.key == 'recaptcha_site_key':
            config.recaptcha_site_key = obj.value
        elif obj.key == 'captcha_usage':
            captcha_usage.append(obj.value)

    if captcha_usage:
        config.captcha_usage = captcha_usage

    return config


async def update(key: str, value: str | list[str]) -> models.Config | None:
    return await repositories.config.update(key=key, value=value)
