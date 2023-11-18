from fastid import repositories, typing
from fastid.repositories import schemes


async def test_create(user: schemes.Users):
    otp = await repositories.otp.create(code='7HUV6DLVICZP27CY7MP75QHSLYB75V72', user_id=user.user_id)
    assert otp.code == '7HUV6DLVICZP27CY7MP75QHSLYB75V72'
    assert otp.user_id == user.user_id


async def test_get_by_user_id(user: schemes.Users):
    otp = await repositories.otp.create(code='7HUV6DLVICZP27CY7MP75QHSLYB75V72', user_id=user.user_id)
    assert otp.code == '7HUV6DLVICZP27CY7MP75QHSLYB75V72'
    assert otp.user_id == user.user_id

    result = await repositories.otp.get_by_user_id(user_id=user.user_id)
    assert result.code == '7HUV6DLVICZP27CY7MP75QHSLYB75V72'
    assert result.user_id == user.user_id


async def test_delete_by_user_id(user: schemes.Users):
    await repositories.otp.create(code='7HUV6DLVICZP27CY7MP75QHSLYB75V72', user_id=user.user_id)
    result = await repositories.otp.delete_by_user_id(user_id=user.user_id)
    assert result

    result = await repositories.otp.delete_by_user_id(user_id=typing.UserID(999))
    assert not result
