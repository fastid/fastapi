from fastapi import APIRouter

from fastid.exceptions import InternalServerException, exception_responses

router = APIRouter(
    tags=['Health check'],
    responses=exception_responses,
)


@router.get(path='/healthcheck/', include_in_schema=False)
async def healthcheck(raise_error: bool = False, internal_server_error: bool = False) -> dict:
    if raise_error:
        raise Exception('Test error')
    if internal_server_error:
        raise InternalServerException

    return {'result': 'success'}
