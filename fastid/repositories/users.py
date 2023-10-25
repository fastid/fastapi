from sqlalchemy import insert, select

from .. import repositories, services, typing
from ..trace import decorator_trace
from . import schemes


@decorator_trace(name='repositories.users.create')
async def create(*, email: typing.Email, password: typing.Password) -> typing.UserID | None:
    hash_password = await services.password_hasher.hasher(password=password)

    async with repositories.db.async_session() as session:
        stmt = insert(schemes.Users).values(email=email, password=hash_password).returning(schemes.Users.user_id)
        result = await session.execute(stmt)
        await session.commit()
        if user_id := result.scalar():
            return typing.UserID(user_id)
        return None


@decorator_trace(name='repositories.users.get_by_email')
async def get_by_email(*, email: typing.Email) -> schemes.Users | None:
    async with repositories.db.async_session() as session:
        stmt = select(schemes.Users).where(schemes.Users.email == email)
        result = await session.scalar(stmt)
        await session.commit()

        if not result:
            return None

        return result
