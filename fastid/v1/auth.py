from fastapi import APIRouter, status
from pydantic import BaseModel, Field

from .. import services, typing
from ..settings import settings

router = APIRouter(tags=['Auth'], prefix='/auth')


class RequestCreateUserByEmail(BaseModel):
    email: typing.Email = Field(..., title='Email address', description='Email address', max_length=200)

    if settings.recaptcha_enable:
        recaptcha_verify: str = Field(..., title='Recaptcha Verify', description='Recaptcha Verify')


class RequestConfirmationCode(BaseModel):
    confirmation_token: str = Field(..., title='JWT Token', description='Confirmation token')
    code: int = Field(..., title='Code', description='Code', examples=[1111])


class ResponseConfirmationToken(BaseModel):
    confirmation_token: str = Field(..., title='JWT Token', description='Confirmation token')


@router.post(
    path='/email/',
    summary='Create a user by email address',
    name='create_user_by_email',
    status_code=status.HTTP_201_CREATED,
)
async def create_user_by_email(body: RequestCreateUserByEmail) -> ResponseConfirmationToken:
    if settings.recaptcha_enable:
        await services.recaptcha.check_verify(recaptcha_verify=body.recaptcha_verify)

    return ResponseConfirmationToken(
        confirmation_token=await services.auth.sending_confirmation_code(email=body.email),
    )


# @router.post(
#     path='/confirmation/',
#     summary='Confirmation code',
#     name='confirmation_code',
# )
# async def confirmation_code(body: RequestConfirmationCode):
#     body.confirmation_token
#     pass
