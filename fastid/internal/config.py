from fastapi import APIRouter

from .. import services
from .models import ResponseConfig

router = APIRouter(prefix='/config')


@router.get(
    path='/',
    summary='Gets the config for the site',
    name='Config for site',
)
async def get_config() -> ResponseConfig:
    config = await services.config.get()
    return ResponseConfig.model_validate(config)
