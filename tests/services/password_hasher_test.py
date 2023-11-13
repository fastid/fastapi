import pytest
from argon2.exceptions import VerifyMismatchError
from pytest_mock import MockerFixture

from fastid import services, typing
from fastid.exceptions import BadRequestException, InternalServerException


async def test_hasher_password_hasher_memory_profile_high():
    password_string = await services.password_hasher.hasher(password=typing.Password('test'))
    assert password_string


async def test_verify():
    password_hash = await services.password_hasher.hasher(password=typing.Password('test'))
    assert await services.password_hasher.verify(password_hash=password_hash, password=typing.Password('test'))


async def test_verify_fail():
    with pytest.raises(InternalServerException):
        await services.password_hasher.verify(password_hash='1234', password=typing.Password('test'))


async def test_verify_mismatch_error(mocker: MockerFixture):
    password_hash = await services.password_hasher.hasher(password=typing.Password('test'))

    mocker.patch('argon2._password_hasher.PasswordHasher.verify', side_effect=VerifyMismatchError)

    with pytest.raises(BadRequestException):
        await services.password_hasher.verify(password_hash=password_hash, password=typing.Password('test'))
