from sqlalchemy import insert, select

from .. import repositories, typing
from ..trace import decorator_trace
from . import schemes


@decorator_trace(name='repositories.users.create')
async def create(*, email: typing.Email, password: typing.Password, admin: bool = False) -> schemes.Users | None:
    async with repositories.db.async_session() as session:
        stmt_user = insert(schemes.Users).values(email=email, password=password, admin=admin).returning(schemes.Users)
        result = await session.execute(stmt_user)

        user = result.scalar()
        if not user:
            raise ValueError('User object not found')

        await session.execute(insert(schemes.Profiles).values(user_id=user.user_id))

        await session.commit()
        return await get_by_id(user_id=user.user_id)


@decorator_trace(name='repositories.users.get_by_id')
async def get_by_id(*, user_id: typing.UserID) -> schemes.Users | None:
    async with repositories.db.async_session() as session:
        stmt = select(schemes.Users).where(schemes.Users.user_id == user_id, schemes.Users.deleted_at.is_(None))
        result = await session.scalar(stmt)
        await session.commit()
        return result


@decorator_trace(name='repositories.users.get_by_email')
async def get_by_email(*, email: typing.Email) -> schemes.Users | None:
    async with repositories.db.async_session() as session:
        stmt = select(schemes.Users).where(schemes.Users.email == email, schemes.Users.deleted_at.is_(None))
        result = await session.scalar(stmt)
        await session.commit()
        return result


@decorator_trace(name='repositories.users.get_all')
async def get_all(*, limit: int = 50, offset: int = 0) -> schemes.Results:
    async with repositories.db.async_session() as session:
        stmt = select(schemes.Users).where(schemes.Users.deleted_at.is_(None)).limit(limit).offset(offset)
        results = await session.scalars(stmt)
        await session.commit()
        return schemes.Results[schemes.Users](items=results.all())
