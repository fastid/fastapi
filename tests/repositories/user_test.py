from pytest_mock import MockerFixture

from fastid import repositories, typing


async def test_create(db_migrations):
    user_id = await repositories.users.create(
        email=typing.Email('user@exmaple.com'),
        password=typing.Password('qwerty'),
    )
    assert user_id


async def test_create_return_none(db_migrations, mocker: MockerFixture):
    mocker.patch('sqlalchemy.Result.scalar', return_value=None)

    user_id = await repositories.users.create(
        email=typing.Email('user@exmaple.com'),
        password=typing.Password('qwerty'),
    )
    assert not user_id


async def test_get_by_email(db_migrations):
    user_id = await repositories.users.create(
        email=typing.Email('user@exmaple.com'),
        password=typing.Password('qwerty'),
    )
    assert user_id

    user = await repositories.users.get_by_email(email='user@exmaple.com')
    assert user.email == typing.Email('user@exmaple.com')
    assert user.user_id
    assert user.password


async def test_get_by_id_not_found(db_migrations):
    user = await repositories.users.get_by_email(email='user@exmaple.com')
    assert user is None


async def test_get_by_id(db_migrations):
    user_id = await repositories.users.create(
        email=typing.Email('user@exmaple.com'),
        password=typing.Password('qwerty'),
    )
    assert user_id

    user = await repositories.users.get_by_id(user_id=user_id)
    assert user.user_id
    assert user.email == typing.Email('user@exmaple.com')
    assert user.created_at
    assert user.updated_at
