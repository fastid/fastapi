import pytest
from pytest_httpx import HTTPXMock

from fastid.context import cxt_ip
from fastid.exceptions import RecaptchaVerifyFailException
from fastid.services.recaptcha import check_verify


async def test_check_verify(httpx_mock: HTTPXMock):
    httpx_mock.add_response(json={'success': True})

    cxt_ip.set('127.0.0.1')
    assert await check_verify(recaptcha_verify='verify')


async def test_check_verify_fail(httpx_mock: HTTPXMock):
    httpx_mock.add_response(json={'success': False})

    cxt_ip.set('127.0.0.1')

    with pytest.raises(RecaptchaVerifyFailException):
        assert await check_verify(recaptcha_verify='verify')
