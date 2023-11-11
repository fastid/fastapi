import pytest
from pytest_mock import MockerFixture

from fastid import password_hasher, repositories, typing
from fastid.exceptions import InternalServerException
from fastid.repositories import schemes


async def test_save(user: schemes.Users):
    user.profile.timezone = 'America/Los_Angeles'
    assert user.profile.timezone == 'America/Los_Angeles'
    await user.profile.save()

    user_new = await repositories.users.get_by_id(user_id=user.user_id)
    assert user_new.profile.timezone == 'America/Los_Angeles'


async def test_get_by_id(user: schemes.Users):
    user_res = await repositories.users.get_by_id(user_id=user.user_id)
    assert user_res.user_id
    assert user_res.email == typing.Email('user@exmaple.com')
    assert user_res.created_at
    assert user_res.updated_at
    assert not user_res.admin


async def test_get_all(user: schemes.Users):
    user_result = await repositories.users.get_all()
    assert int(user_result) == 1

    for user in user_result:
        assert user.user_id
        assert user.email == typing.Email('user@exmaple.com')
        assert user.created_at
        assert user.updated_at
        break


async def test_get_by_email(user: schemes.Users):
    user = await repositories.users.get_by_email(email='user@exmaple.com')
    assert user.user_id
    assert user.email == typing.Email('user@exmaple.com')
    assert user.created_at
    assert user.updated_at


async def test_password_verify(user: schemes.Users):
    user.password = await password_hasher.hasher(password=user.password)
    await user.save()
    assert await user.password_verify(password=typing.Password('qwerty'))


async def test_locate_language(user: schemes.Users):
    await user.profile.set_locate(locate=typing.Locate.EN_GB)

    user_res = await repositories.users.get_by_id(user_id=user.user_id)
    assert user_res.profile.locate == typing.Locate.EN_GB
    assert user_res.profile.language == typing.Language.EN


async def test_get_primary_key(user: schemes.Users, mocker: MockerFixture):
    mocker.patch('fastid.repositories.schemes.Base.get_primary_key', return_value=None)
    user.profile.first_name = 'Lily'
    with pytest.raises(InternalServerException):
        await user.profile.save()
