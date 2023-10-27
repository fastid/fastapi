from fastapi import APIRouter, status

from .. import services
from . import models

router = APIRouter(tags=['Users'], prefix='/users')


@router.post(
    path='/refresh_token/',
    name='Updates refresh token',
    description='This method is used to update the refresh tokens that are used for the dashboard',
)
async def updates_refresh_token(body: models.RequestUsersRefreshToken) -> models.ResponseUsersRefreshToken:
    token = await services.tokens.refresh(refresh_token=body.refresh_token, audience='internal')

    return models.ResponseUsersRefreshToken(
        access_token=token.access_token,
        refresh_token=token.refresh_token,
        token_type=token.token_type,
        expires_in=token.expires_in,
    )


@router.post(
    path='/signin/',
    summary='SignIn user',
    name='user_signin',
    status_code=status.HTTP_201_CREATED,
)
async def signin_user(body: models.RequestUserSignin):
    await services.recaptcha.check_verify(recaptcha_verify=body.captcha)
    print(body)
    return {}
