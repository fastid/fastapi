from fastapi import APIRouter

from .. import services
from . import models

router = APIRouter(prefix='/config')


@router.get(
    path='/',
    summary='Gets the config for the site',
    name='Config for site',
)
async def get_config() -> models.Response.Config:
    return models.Response.Config.model_validate(await services.config.get())
