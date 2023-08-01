from fastapi import APIRouter, status

from .. import services
from ..settings import settings
from . import schemes

router = APIRouter(tags=['Users'], prefix='/users')


@router.post(
    path='/email/',
    summary='Create a user by email address',
    name='create_user_by_email',
    status_code=status.HTTP_201_CREATED,
)
async def create_user_by_email(body: schemes.RequestCreateUserByEmail) -> schemes.ResponseEmpty:
    if settings.recaptcha_enable:
        await services.recaptcha.check_verify(recaptcha_verify=body.recaptcha_verify)

    await services.user.create_by_email(email=body.email, password=body.password)

    return schemes.ResponseEmpty()
