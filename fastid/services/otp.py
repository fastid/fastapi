import pyotp
from pydantic import AnyUrl

from .. import repositories, typing
from ..settings import settings
from ..trace import decorator_trace
from . import models


@decorator_trace(name='otp.create')
async def create(*, user_id: typing.UserID) -> models.OTP | None:
    otp = await get_by_user_id(user_id=user_id)
    if otp is None:
        code = pyotp.random_base32()
        otpauth = pyotp.totp.TOTP(code).provisioning_uri(name=settings.jwt_iss, issuer_name='Secure App')

        await repositories.otp.create(user_id=user_id, code=code)
        return models.OTP(code=code, otpauth=AnyUrl(otpauth))

    return None


@decorator_trace(name='otp.get_by_user_id')
async def get_by_user_id(*, user_id: typing.UserID) -> models.OTP | None:
    otp = await repositories.otp.get_by_user_id(user_id=user_id)
    if otp is None:
        return None

    otpauth = pyotp.totp.TOTP(otp.code).provisioning_uri(name=settings.jwt_iss, issuer_name='Secure App')
    return models.OTP(code=otp.code, otpauth=AnyUrl(otpauth))
