from unittest.mock import PropertyMock, patch

import pytest

from fastid import services, typing
from fastid.exceptions import InternalServerException
from fastid.settings import PasswordHasherMemoryProfile


async def test_hasher_password_hasher_memory_profile_low():
    with patch('fastid.settings.settings.password_hasher_memory_profile', new_callable=PropertyMock) as mock_foo:
        mock_foo.return_value = PasswordHasherMemoryProfile.low

        password_string = await services.password_hasher.hasher(password=typing.Password('test'))
        assert password_string


async def test_hasher_password_hasher_memory_profile_high():
    password_string = await services.password_hasher.hasher(password=typing.Password('test'))
    assert password_string


async def test_verify():
    password_hash = await services.password_hasher.hasher(password=typing.Password('test'))
    assert await services.password_hasher.verify(password_hash=password_hash, password=typing.Password('test'))


async def test_verify_fail():
    with pytest.raises(InternalServerException):
        await services.password_hasher.verify(password_hash='1234', password=typing.Password('test'))
