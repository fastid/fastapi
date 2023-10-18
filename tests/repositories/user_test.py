from fastid import repositories, typing


async def test_create(db_migrations):
    await repositories.users.create(email=typing.Email('kostya@yandex.ru'), password=typing.Password('qwerty'))
