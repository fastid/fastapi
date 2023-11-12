import pytest
from pytest_mock import MockerFixture

from fastid import services, typing
from fastid.exceptions import BadRequestException, NotFoundException
from fastid.services import models


async def test_create(user: models.User):
    token = await services.tokens.create(audience='test_audience', user_id=user.user_id)
    assert token.access_token
    assert token.refresh_token
    assert token.token_type
    assert token.expires_in


async def test_reload(user: models.User):
    token = await services.tokens.create(audience='test_audience', user_id=user.user_id)
    token = await services.tokens.reload(refresh_token=token.refresh_token, audience='test_audience')
    assert token.access_token
    assert token.refresh_token
    assert token.token_type
    assert token.expires_in


async def test_update_exception(user: models.User):
    with pytest.raises(NotFoundException):
        await services.tokens.reload(refresh_token='fake_token', audience='test_audience')


async def test_get(user: models.User):
    token = await services.tokens.create(audience='test_audience', user_id=user.user_id)
    token_result = await services.tokens.get(jwt_token=token.access_token, audience='test_audience')
    assert token_result.token_id


async def test_delete_by_id(user: models.User):
    token = await services.tokens.create(audience='test_audience', user_id=user.user_id)
    await services.tokens.delete_by_id(token_id=token.token_id)

    with pytest.raises(NotFoundException):
        await services.tokens.get(jwt_token=token.access_token)


async def test_signin(user: models.User):
    token = await services.tokens.signin(email=typing.Email('user@exmaple.com'), password=typing.Password('password'))
    assert token.refresh_token
    assert token.access_token
    assert token.token_type == 'Bearer'
    assert token.expires_in


async def test_bad_request(user: models.User, mocker: MockerFixture):
    mocker.patch('fastid.services.users.get_by_email', return_value=None)

    with pytest.raises(BadRequestException):
        await services.tokens.signin(email=typing.Email('user@exmaple.com'), password=typing.Password('password'))


async def test_bad_request_password_hasher(user: models.User, mocker: MockerFixture):
    mocker.patch('fastid.services.password_hasher.verify', side_effect=BadRequestException)

    with pytest.raises(BadRequestException):
        await services.tokens.signin(email=typing.Email('user@exmaple.com'), password=typing.Password('password'))
