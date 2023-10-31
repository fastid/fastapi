from typing import Annotated, AsyncGenerator

from fastapi import Depends, Security
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from . import services, typing
from .context import cxt_user_id

access_token_security = Security(HTTPBearer(description='Waiting for the transfer of the access token'))


async def __auth_user(
    header: HTTPAuthorizationCredentials = access_token_security,
) -> AsyncGenerator[services.models.Token | None, None]:
    token = await services.tokens.get(jwt_token=header.credentials, audience='internal')

    cxt_user_id_token = cxt_user_id.set(token.user_id)
    yield token.user_id
    cxt_user_id.reset(cxt_user_id_token)


auth_user_depends = Annotated[typing.UserID, Depends(__auth_user)]
