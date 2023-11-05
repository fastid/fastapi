from fastapi import APIRouter, status

from .. import services, typing
from ..depends import auth_user_depends, token_id_depends
from ..settings import settings
from . import models

router = APIRouter()


@router.post(
    path='/refresh_token/',
    name='Updates refresh token',
    description='This method is used to update the refresh tokens that are used for the dashboard',
    status_code=status.HTTP_201_CREATED,
)
async def updates_refresh_token(body: models.RequestUsersRefreshToken) -> models.ResponseUsersRefreshToken:
    token = await services.tokens.update(refresh_token=body.refresh_token, audience='internal')

    return models.ResponseUsersRefreshToken(
        access_token=token.access_token,
        refresh_token=token.refresh_token,
        token_type=token.token_type,
        expires_in=token.expires_in,
    )


@router.post(
    path='/signin/',
    summary='Sign in user',
    name='user_signin',
    status_code=status.HTTP_201_CREATED,
)
async def signin_user(body: models.RequestUserSignin) -> models.ResponseUserSignin:
    if settings.captcha and settings.captcha == 'recaptcha' and 'signin' in settings.captcha_usage.split(','):
        await services.recaptcha.check_verify(recaptcha_verify=body.captcha)

    token = await services.users.signin(email=body.email, password=body.password)

    return models.ResponseUserSignin(
        access_token=token.access_token,
        refresh_token=token.refresh_token,
        expires_in=token.expires_in,
        token_type=token.token_type,
    )


@router.get(
    path='/info/',
    summary='Info user',
    name='user_info',
)
async def info(user_id: auth_user_depends) -> models.ResponseUserInfo:
    user = await services.users.get_by_id(user_id=typing.UserID(user_id))
    return models.ResponseUserInfo(user_id=typing.UserID(user_id), email=typing.Email(user.email))


@router.post(
    path='/logout/',
    summary='Logout',
    name='user_logout',
)
async def logout(token_id: token_id_depends, body: models.RequestEmply) -> models.ResponseEmply:
    await services.tokens.delete_by_id(token_id=token_id)
    return models.ResponseEmply()
