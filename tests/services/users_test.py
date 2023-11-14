from datetime import date

import pytest
from pytest_mock import MockerFixture

from fastid import services, typing
from fastid.exceptions import NotFoundException
from fastid.services import models


async def test_get_by_id(user: models.User):
    user = await services.users.get_by_id(user_id=user.user_id)
    assert isinstance(user, models.User)

    assert user is not None
    assert user.user_id
    assert user.email == typing.Email('user@exmaple.com')
    assert user.password
    assert user.created_at
    assert user.updated_at

    assert user.profile
    assert user.profile.language == typing.Language.EN
    assert user.profile.locate == typing.Locate.EN_US
    assert user.profile.timezone == 'UTC'


async def test_get_by_id_object_none(user: models.User, mocker: MockerFixture):
    mocker.patch('fastid.repositories.users.get_by_id', return_value=None)
    user = await services.users.get_by_id(user_id=user.user_id)
    assert user is None


async def test_get_by_email(user: models.User):
    user = await services.users.get_by_email(email=typing.Email(user.email))
    assert isinstance(user, models.User)

    assert user is not None
    assert user.user_id
    assert user.email == typing.Email('user@exmaple.com')
    assert user.password
    assert user.created_at
    assert user.updated_at

    assert user.profile

    assert user.profile.language == typing.Language.EN
    assert user.profile.locate == typing.Locate.EN_US
    assert user.profile.timezone == 'UTC'


async def test_get_by_email_object_none(user: models.User, mocker: MockerFixture):
    mocker.patch('fastid.repositories.users.get_by_email', return_value=None)
    user = await services.users.get_by_email(email=typing.Email(user.email))
    assert user is None


async def test_change_locate(user: models.User):
    await services.users.change_locate(user_id=user.user_id, locate=typing.Locate.EN_GB)
    user = await services.users.get_by_id(user_id=user.user_id)
    if user.profile:
        assert user.profile.locate == typing.Locate.EN_GB
        assert user.profile.language == typing.Language.EN

    with pytest.raises(NotFoundException):
        await services.users.change_locate(user_id=typing.UserID(9999), locate=typing.Locate.EN_GB)


async def test_change_timezone(user: models.User):
    await services.users.change_timezone(user_id=user.user_id, timezone='America/Los_Angeles')

    user = await services.users.get_by_id(user_id=user.user_id)
    if user.profile:
        assert user.profile.timezone == 'America/Los_Angeles'

    with pytest.raises(NotFoundException):
        await services.users.change_timezone(user_id=typing.UserID(9999), timezone='America/Los_Angeles')

    with pytest.raises(NotFoundException):
        await services.users.change_timezone(user_id=user.user_id, timezone='America/Los_Angeles_fake')


async def test_profile_save(user: models.User):
    await services.users.profile_save(
        user_id=user.user_id,
        first_name='John',
        last_name='Doe',
        date_birth=date(year=2000, month=1, day=1),
        gender=typing.Gender.MALE,
    )

    user = await services.users.get_by_id(user_id=user.user_id)
    if user.profile:
        assert user.profile.first_name == 'John'
        assert user.profile.last_name == 'Doe'
        assert str(user.profile.date_birth) == '2000-01-01'
        assert user.profile.gender == typing.Gender.MALE

    with pytest.raises(NotFoundException):
        await services.users.profile_save(
            user_id=typing.UserID(9999),
            first_name='John',
            last_name='Doe',
            date_birth=date(year=2000, month=1, day=1),
            gender=typing.Gender.MALE,
        )
