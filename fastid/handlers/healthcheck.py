from fastapi import APIRouter

router = APIRouter(tags=['Health check'])


@router.get(path='/healthcheck/', include_in_schema=False)
async def healthcheck(raise_error: bool = False) -> dict:
    if raise_error:
        raise Exception('Test error')
    return {'result': 'success'}
