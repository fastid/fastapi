from random import randint
from urllib import parse

from .. import repositories
from ..exceptions import BadRequestException


async def creating_link_redirect_code(*, client_id: str, redirect_uri: str, state: str | None = None) -> str:
    code = randint(1111111, 9999999)
    redirect_uri = redirect_uri.lower().strip()

    application = await repositories.applications.get_by_client_id(client_id=client_id)

    flag_found_redirect_uri = False
    for application_uri in application.redirect_uri:
        if application_uri.uri == redirect_uri:
            flag_found_redirect_uri = True

    if not flag_found_redirect_uri:
        raise BadRequestException

    params = {'code': code}
    if state is not None:
        params['state'] = state

    redirect_uri = redirect_uri.rstrip('/')
    return f'{redirect_uri}/?{parse.urlencode(params)}'
