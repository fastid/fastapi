from ..context import cxt_ip
from ..exceptions import RecaptchaVerifyFailException
from ..http_base_client import http_base_client
from ..settings import settings
from ..trace import decorator_trace

URL = 'https://www.google.com/'


@decorator_trace(name='services.recaptcha.check_verify')
async def check_verify(*, recaptcha_verify: str) -> bool:
    async with http_base_client(base_url=URL) as client:
        params = {
            'secret': settings.recaptcha_secret_key,
            'response': recaptcha_verify,
        }

        if ip := cxt_ip.get():
            params['remoteip'] = ip

        response = await client.post(url='recaptcha/api/siteverify', params=params)

        if not response.json().get('success'):
            raise RecaptchaVerifyFailException(i18n='recaptcha_verify_fail')

        return True
