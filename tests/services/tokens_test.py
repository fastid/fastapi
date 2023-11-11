import pytest

from fastid import services, typing
from fastid.exceptions import NotFoundException
from fastid.services import models


async def test_create(user: models.User):
    jwt_token = await services.tokens.create(audience='test_audience', user_id=user.user_id)
    assert jwt_token.access_token
    assert jwt_token.refresh_token
    assert jwt_token.token_type
    assert jwt_token.expires_in


async def test_reload(user: models.User):
    jwt_token = await services.tokens.create(audience='test_audience', user_id=user.user_id)
    token = await services.tokens.reload(refresh_token=jwt_token.refresh_token, audience='test_audience')
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


async def test_signin(user: models.User):
    token = await services.tokens.signin(email=typing.Email('user@exmaple.com'), password=typing.Password('password'))
    assert token.refresh_token
    assert token.access_token
    assert token.token_type == 'Bearer'
    assert token.expires_in
