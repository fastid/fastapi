from pytest_mock import MockerFixture

from fastid import repositories, typing


async def test_create(db_migrations):
    user_id = await repositories.users.create(
        email=typing.Email('kostya@yandex.ru'),
        password=typing.Password('qwerty'),
    )
    assert user_id


async def test_create_return_none(db_migrations, mocker: MockerFixture):
    mocker.patch('sqlalchemy.Result.scalar', return_value=None)

    user_id = await repositories.users.create(
        email=typing.Email('kostya@yandex.ru'),
        password=typing.Password('qwerty'),
    )
    assert not user_id
