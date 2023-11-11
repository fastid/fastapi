from fastid import services, typing
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


# async def test_signin(user: models.User):
#     token = await services.users.signin(email=typing.Email('user@exmaple.com'), password=typing.Password('password'))
#     assert token.refresh_token
#     assert token.access_token
#     assert token.token_type


# async def test_get_by_id2(db_migrations):
#     user_id = await services.users.create(
#         email=typing.Email('user@exmaple.com'),
#         password=typing.Password('password'),
#     )
#     user = await services.users.get_by_id(user_id=user_id)
#     assert user.user_id
#     assert user.email == typing.Email('user@exmaple.com')
#
#
# async def test_get_by_id_not_found(db_migrations):
#     user = await services.users.get_by_id(user_id=typing.UserID(99))
#     assert not user


# async def test_exception(db_migrations):
#     with pytest.raises(BadRequestException):
#         await services.users.signin(email=typing.Email('user@exmaple.com'), password=typing.Password('password'))
#
#     await services.users.create(
#         email=typing.Email('user@exmaple.com'),
#         password=typing.Password('password'),
#     )
#
#     with pytest.raises(BadRequestException):
#         await services.users.signin(email=typing.Email('user@exmaple.com'), password=typing.Password('password_fail'))
