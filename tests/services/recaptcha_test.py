from fastid.context import cxt_ip
from fastid.services.recaptcha import check_verify


async def test_check_verify():
    cxt_ip.set('127.0.0.1')
    assert await check_verify(recaptcha_verify='1111')
