from fastid import repositories
from fastid.repositories import schemes


async def test_get_by_id(token: schemes.Tokens):
    token = await repositories.tokens.get_by_id(token_id=token.token_id)

    assert token
    assert isinstance(token, repositories.schemes.Tokens)
    assert token.token_id
    assert token.access_token == 'access_token'
    assert token.refresh_token == 'refresh_token'
    assert token.user_id
    assert token.expires_at
    assert token.created_at
    assert token.updated_at


async def test_delete_by_id(token: schemes.Tokens):
    result_delete = await repositories.tokens.delete_by_id(token_id=token.token_id)
    assert result_delete

    result_delete = await repositories.tokens.delete_by_id(token_id=token.token_id)
    assert not result_delete

    result_token = await repositories.tokens.get_by_id(token_id=token.token_id)
    assert not result_token


# async def test_create_return_none(db_migrations, mocker: MockerFixture):
#     user_id = await repositories.users.create(
#         email=typing.Email('user@exmaple.com'),
#         password=typing.Password('Password'),
#     )
#
#     mocker.patch('sqlalchemy.Result.scalar', return_value=None)
#
#     token_id = await repositories.tokens.create(
#         token_id=typing.TokenID(uuid.uuid4()),
#         access_token='access_token',
#         refresh_token='refresh_token',
#         user_id=user_id,
#         expires_at=datetime.datetime.now(tz=ZoneInfo('UTC')) + timedelta(days=1),
#     )
#     assert not token_id
#
#
# async def test_get_by_id(db_migrations):
#     user_id = await repositories.users.create(
#         email=typing.Email('user@exmaple.com'),
#         password=typing.Password('Password'),
#     )
#
#     token_id = await repositories.tokens.create(
#         token_id=typing.TokenID(uuid.uuid4()),
#         access_token='access_token',
#         refresh_token='refresh_token',
#         user_id=user_id,
#         expires_at=datetime.datetime.now(tz=ZoneInfo('UTC')) + timedelta(days=1),
#     )
#     token = await repositories.tokens.get_by_id(token_id=token_id)
#     assert token.token_id == token_id
#     assert token.access_token == 'access_token'
#     assert token.refresh_token == 'refresh_token'
#     assert token.user_id == user_id
#     assert token.expires_at
#
#
# async def test_get_by_id_mot_found(db_migrations):
#     with pytest.raises(NotFoundException):
#         await repositories.tokens.get_by_id(token_id=typing.TokenID(uuid.uuid4()))
#
#
# async def test_delete_by_id(db_migrations):
#     user_id = await repositories.users.create(
#         email=typing.Email('user@exmaple.com'),
#         password=typing.Password('Password'),
#     )
#
#     token_id = await repositories.tokens.create(
#         token_id=typing.TokenID(uuid.uuid4()),
#         access_token='access_token',
#         refresh_token='refresh_token',
#         user_id=user_id,
#         expires_at=datetime.datetime.now(tz=ZoneInfo('UTC')) + timedelta(days=1),
#     )
#     token_is_delete = await repositories.tokens.delete_by_id(token_id=token_id)
#     assert token_is_delete
#
#     token_is_delete_not_found = await repositories.tokens.delete_by_id(token_id=typing.TokenID(uuid.uuid4()))
#     assert not token_is_delete_not_found
