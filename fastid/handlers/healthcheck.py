from fastapi import APIRouter

from fastid.exceptions import exception_responses

router = APIRouter(
    tags=['Health check'],
    responses=exception_responses,
)


@router.get(path='/healthcheck/', include_in_schema=False)
async def healthcheck(raise_error: bool = False) -> dict:
    if raise_error:
        raise Exception('Test error')
    return {'result': 'success'}
