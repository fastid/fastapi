import httpx

from ..exceptions import RecaptchaVerifyFailException
from ..http_base_client import http_base_client
from ..settings import settings
from ..context import cxt_ip

URL = 'https://www.google.com/'


async def check_verify(recaptcha_verify: str) -> bool:
    async with http_base_client(base_url=URL) as client:
        client: httpx.AsyncClient

        params = {
            'secret': settings.recaptcha_secret_key,
            'response': recaptcha_verify,
        }

        if ip := cxt_ip.get():
            params['remoteip'] = ip

        response = await client.post(url='recaptcha/api/siteverify', params=params)

        if response.json().get('success'):
            return True

        raise RecaptchaVerifyFailException()
