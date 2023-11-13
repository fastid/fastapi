from fastapi import APIRouter, status
from pydantic import BaseModel, ConfigDict, Field

from .. import services, typing
from ..depends import auth_user_internal_token_depends
from ..exceptions import exception_responses
from ..settings import settings

router = APIRouter(responses=exception_responses)


class SigninRequest(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    email: typing.Email = Field(..., title='Email address', description='Email address')
    password: typing.Password = Field(
        ...,
        title='Password',
        description='Password',
    )
    captcha: str | None = Field(
        None,
        title='Captcha',
        description='Captcha',
    )


class SigninResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    access_token: str
    refresh_token: str
    expires_in: int
    token_type: str = 'Bearer'


class RefreshTokenRequest(BaseModel):
    refresh_token: str


class RefreshTokenUsers(SigninResponse):
    pass


class EmptyResponse(BaseModel):
    pass


class EmptyRequest(BaseModel):
    pass


@router.post(
    path='/signin/',
    summary='Sign in',
    status_code=status.HTTP_201_CREATED,
)
async def signin(body: SigninRequest) -> SigninResponse:
    if settings.captcha and settings.captcha == 'recaptcha' and 'signin' in settings.captcha_usage.split(','):
        await services.recaptcha.check_verify(recaptcha_verify=body.captcha)

    token = await services.tokens.signin(email=body.email, password=body.password)
    return SigninResponse.model_validate(token)


@router.post(
    path='/refresh_token/',
    summary='Updates refresh token',
    description='This method is used to update the refresh tokens that are used for the dashboard',
    status_code=status.HTTP_201_CREATED,
)
async def updates_refresh_token(body: RefreshTokenRequest) -> RefreshTokenUsers:
    token = await services.tokens.reload(refresh_token=body.refresh_token, audience='internal')
    return RefreshTokenUsers.model_validate(token)


@router.post(
    path='/logout/',
    summary='Logout',
    name='user_logout',
)
async def logout(token_id: auth_user_internal_token_depends, body: EmptyRequest) -> EmptyResponse:
    await services.tokens.delete_by_id(token_id=token_id)
    return EmptyResponse()


# @router.get(
#     path='/info/',
#     summary='Info user',
#     name='user_info',
# )
# async def info(user_id: auth_user_depends) -> models.ResponseUserInfo:
#     user = await services.users.get_by_id(user_id=typing.UserID(user_id))
#     return models.ResponseUserInfo.model_validate(user)
#
#

#
#
# @router.get(
#     path='/language/',
#     summary='language',
#     name='language_get',
# )
# async def language_get(user_id: auth_user_depends) -> models.ResponseList[models.ResponseLanguage]:
#     languages = await services.language.get_all()
#     return models.ResponseList[models.ResponseLanguage].model_validate({'results': languages})
#
#
# @router.post(
#     path='/language/',
#     summary='language',
#     name='language_post',
# )
# async def language_get(user_id: auth_user_depends, body: models.Request.Empty) -> models.Response.Empty:
#     await services.language.upgrade(user_id=user_id, language=body.language, locate=body.locate)
#     return models.Response.Empty()
#
#
# @router.get(
#     path='/timezone/',
#     summary='timezone',
#     name='timezone_get',
# )
# async def timezone_get(body: models.Request.Empty) -> models.Response.Empty:
#     import zoneinfo
#
#     zones = zoneinfo.available_timezones()
#     return sorted(zones)
