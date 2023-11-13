from argon2 import PasswordHasher
from argon2.exceptions import InvalidHash, VerifyMismatchError
from argon2.profiles import RFC_9106_HIGH_MEMORY
from async_lru import alru_cache

from fastid import typing
from fastid.exceptions import BadRequestException, InternalServerException
from fastid.trace import decorator_trace


@decorator_trace(name='password_hasher._get_password_hasher')
@alru_cache(maxsize=64)
async def _get_password_hasher() -> PasswordHasher:
    return PasswordHasher(
        time_cost=RFC_9106_HIGH_MEMORY.time_cost,
        memory_cost=RFC_9106_HIGH_MEMORY.memory_cost,
        parallelism=RFC_9106_HIGH_MEMORY.parallelism,
        hash_len=RFC_9106_HIGH_MEMORY.hash_len,
        salt_len=RFC_9106_HIGH_MEMORY.salt_len,
    )


@decorator_trace(name='password_hasher.hasher')
async def hasher(*, password: typing.Password) -> typing.Password:
    ph = await _get_password_hasher()
    return typing.Password(ph.hash(password=password))


@decorator_trace(name='password_hasher.verify')
async def verify(*, password_hash: str, password: typing.Password) -> bool:
    ph = await _get_password_hasher()

    try:
        ph.verify(password_hash, password)
    except InvalidHash as err:
        raise InternalServerException(i18n='password_incorrect', message='Password is incorrect') from err
    except VerifyMismatchError as err:
        raise BadRequestException(i18n='password_incorrect', message='Password is incorrect') from err

    return True
