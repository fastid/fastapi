from fastapi import APIRouter, status

from .. import services
from . import models

router = APIRouter(tags=['Admin'], prefix='/admin')


@router.post(
    path='/signup/',
    summary='Create a admin user',
    name='create_admin_user',
    status_code=status.HTTP_201_CREATED,
)
async def create_user(body: models.RequestCreateAdminUser) -> models.ResponseCreateAdminUser:
    token = await services.admin.create_user(email=body.email, password=body.password)

    return models.ResponseCreateAdminUser(
        access_token=token.access_token,
        refresh_token=token.refresh_token,
        token_type=token.token_type,
        expires_in=token.expires_in,
    )
