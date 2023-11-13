from typing import Annotated, AsyncGenerator

from fastapi import Depends, Security
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from . import services, typing
from .context import cxt_user_id
from .exceptions import MainException, UnauthorizedException

access_token_security = Security(
    HTTPBearer(
        description='Waiting for the transfer of the access token',
        auto_error=False,
    ),
)


async def __auth_user_internal(
    header: HTTPAuthorizationCredentials = access_token_security,
) -> AsyncGenerator[typing.UserID | None, None]:
    if header is None:
        raise UnauthorizedException(message='Invalid token', i18n='invalid_token')

    try:
        token = await services.tokens.get(jwt_token=header.credentials, audience='internal')
    except MainException as err:
        raise UnauthorizedException(message='Invalid token', i18n='invalid_token') from err

    cxt_token = cxt_user_id.set(token.user_id)
    yield token.user_id
    cxt_user_id.reset(cxt_token)


async def __auth_user_internal_token(
    header: HTTPAuthorizationCredentials = access_token_security,
) -> AsyncGenerator[typing.TokenID | None, None]:
    if header is None:
        raise UnauthorizedException(message='Invalid token', i18n='invalid_token')

    try:
        token = await services.tokens.get(jwt_token=header.credentials, audience='internal')
    except MainException as err:
        raise UnauthorizedException(message='Invalid token', i18n='invalid_token') from err

    yield token.token_id


auth_user_internal_depends = Annotated[typing.UserID, Depends(__auth_user_internal)]
auth_user_internal_token_depends = Annotated[typing.UserID, Depends(__auth_user_internal_token)]
