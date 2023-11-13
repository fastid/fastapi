from fastapi import APIRouter

from .. import services
from ..exceptions import exception_responses

router = APIRouter(prefix='/config', responses=exception_responses)


class ConfigResponse(services.models.Config):
    pass


@router.get(
    path='/',
    summary='Gets the config for the site',
    name='Config for site',
)
async def get_config() -> ConfigResponse:
    return ConfigResponse.model_validate(await services.config.get())
