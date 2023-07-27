from fastapi import APIRouter

from .. import services
from ..exceptions import RecaptchaVerifyFailException
from ..settings import settings
from . import schemes

router = APIRouter(tags=['Users'], prefix='/users')


@router.post(
    path='/email/',
    summary='Create a user by email address',
    name='create_user_by_email_address',
)
async def create_user_by_email(body: schemes.RequestCreateUserByEmail) -> schemes.ResponseEmpty:
    if settings.recaptcha_enable:
        await services.recaptcha.check_verify(recaptcha_verify=body.recaptcha_verify)

    return schemes.ResponseEmpty()
