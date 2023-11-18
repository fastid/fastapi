from sqlalchemy import delete, insert, select

from .. import repositories, typing
from ..trace import decorator_trace
from . import schemes


@decorator_trace(name='repositories.otp.create')
async def create(*, code: str, user_id: typing.UserID) -> schemes.OTP | None:
    stmt = (
        insert(schemes.OTP)
        .values(
            code=code,
            user_id=user_id,
        )
        .returning(schemes.OTP)
    )

    async with repositories.db.async_session() as session:
        result = await session.execute(stmt)
        await session.commit()
        return result.scalar()


@decorator_trace(name='repositories.otp.get_by_user_id')
async def get_by_user_id(*, user_id: typing.UserID) -> schemes.OTP | None:
    stmt = select(schemes.OTP).where(schemes.OTP.user_id == user_id).limit(1)
    async with repositories.db.async_session() as session:
        return await session.scalar(stmt)


@decorator_trace(name='repositories.otp.delete_by_user_id')
async def delete_by_user_id(*, user_id: typing.UserID) -> bool:
    stmt = delete(schemes.OTP).where(schemes.OTP.user_id == user_id)
    async with repositories.db.async_session() as session:
        result = await session.execute(stmt)
        await session.commit()

        if result.rowcount:
            return True
        return False
