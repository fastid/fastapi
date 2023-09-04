import string
from enum import Enum
from random import choice
from typing import Annotated

from fastapi import APIRouter
from fastapi.params import Form, Query
from starlette.responses import RedirectResponse

from .. import services

router = APIRouter(tags=['OAuth'], prefix='/oauth')


class ResponseType(str, Enum):
    code: str = 'code'  # Authorization Code Flow
    token: str = 'token'  # Implicit Flow


class GrantType(str, Enum):
    authorization_code: str = 'authorization_code'  # Authorization Code Flow
    password: str = 'password'  # Password Grant
    client_credentials: str = 'client_credentials'  # Client Credentials
    refresh_token: str = 'refresh_token'


def random_string(length: int) -> str:
    letters = string.ascii_lowercase
    return ''.join(choice(letters) for i in range(length))


@router.get(path='/authorize/')
async def authorize(
    client_id: Annotated[str, Query()],
    redirect_uri: Annotated[str, Query()],
    response_type: Annotated[ResponseType, Query()] = 'code',
    state: Annotated[str | None, Query()] = None,
) -> RedirectResponse:
    if response_type == ResponseType.code:
        link = await services.oauth.creating_link_redirect_code(
            client_id=client_id,
            redirect_uri=redirect_uri,
            state=state,
        )

        return RedirectResponse(url=link)
    return None


@router.post(path='/token/')
async def token(
    client_id: Annotated[str, Form()],
    client_secret: Annotated[str, Form()],
    grant_type: Annotated[GrantType, Form()] = 'authorization_code',
    code: Annotated[str | None, Form()] = None,
) -> dict:
    pass


@router.post(path='/revoke_token/')
async def revoke_token(access_token: Annotated[str, Form()]) -> dict:
    pass
