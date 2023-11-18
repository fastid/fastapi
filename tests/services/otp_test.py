from fastid import services
from fastid.services import models


async def test_create(user: models.User):
    otp = await services.otp.create(user_id=user.user_id)
    assert otp.code
    assert otp.otpauth

    otp = await services.otp.create(user_id=user.user_id)
    assert otp is None
