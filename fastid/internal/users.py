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


class SessionResponse(BaseModel):
    session_key: str
    totp: bool = False


class SigninSessionKeyRequest(BaseModel):
    totp: int | None = None


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
async def signin(body: SigninRequest) -> SessionResponse:
    if settings.captcha and settings.captcha == 'recaptcha' and 'signin' in settings.captcha_usage.split(','):
        await services.recaptcha.check_verify(recaptcha_verify=body.captcha)

    session = await services.users.signin(email=body.email, password=body.password)
    return SessionResponse(session_key=session.session_key)


@router.post(
    path='/signin/{session_key}/',
    summary='Sign in',
    status_code=status.HTTP_201_CREATED,
)
async def signin_session(body: SigninSessionKeyRequest, session_key: str) -> SigninResponse:
    token = await services.users.signin_session(session_key=session_key)
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
