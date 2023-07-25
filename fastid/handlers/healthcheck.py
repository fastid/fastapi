import httpx
from fastapi import APIRouter

from ..http_base_client import http_base_client

router = APIRouter(tags=['Health check'])


@router.get(path='/healthcheck/', include_in_schema=False)
async def healthcheck() -> dict:
    return {'result': 'success'}
