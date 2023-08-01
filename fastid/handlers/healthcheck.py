from fastapi import APIRouter

router = APIRouter(tags=['Health check'])


@router.get(path='/healthcheck/', include_in_schema=False)
async def healthcheck() -> dict:
    return {'result': 'success'}
