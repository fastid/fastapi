import re
from datetime import date, datetime
from typing import Generator, Generic, Sequence, TypeVar
from uuid import UUID

from sqlalchemy import (
    JSON,
    Boolean,
    Date,
    DateTime,
    Enum,
    ForeignKey,
    Integer,
    String,
    Text,
    Uuid,
    func,
    inspect,
    update,
)
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship

from .. import typing
from ..exceptions import InternalServerException
from ..services import password_hasher
from . import db

T_Results = TypeVar('T_Results')


class Base(DeclarativeBase):
    _edited: dict[str, str | typing.Gender | typing.Locate | typing.Locate] = {}

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=func.now(),
        sort_order=20,
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=func.now(),
        onupdate=func.now(),
        sort_order=30,
    )

    deleted_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
        sort_order=40,
    )

    def get_primary_key(self) -> str | None:
        _inspect = inspect(self)
        model_columns = _inspect.mapper.columns

        primary_key = None
        for column in model_columns:
            if column.primary_key:
                primary_key = column.key
                break
        return primary_key

    async def save(self) -> None:
        primary_key = self.get_primary_key()

        if not primary_key:
            raise InternalServerException('Not found primary key')

        _inspect = inspect(self)
        if hasattr(_inspect, 'committed_state'):
            values = {}
            for key in _inspect.committed_state:
                values[key] = getattr(self, key)

            if values:
                stmt = (
                    update(self.__class__)
                    .where(getattr(self.__class__, primary_key) == getattr(self, primary_key))
                    .values(**values)
                )

                async with db.async_session() as session:
                    await session.execute(stmt)
                    await session.commit()


class Results(Generic[T_Results]):
    def __init__(self, items: Sequence[T_Results]) -> None:
        self.items: Sequence[T_Results] = items

    def __iter__(self) -> Generator[T_Results, None, None]:
        for item in self.items:
            yield item

    def __int__(self) -> int:
        return len(self.items)


class Users(Base):
    __tablename__ = 'users'

    user_id: Mapped[typing.UserID] = mapped_column(Integer, primary_key=True, autoincrement=True, sort_order=10)
    email: Mapped[typing.Email] = mapped_column(String(200), unique=True, nullable=True, sort_order=60)
    password: Mapped[str] = mapped_column(String(200), nullable=True, sort_order=70)
    # phone: Mapped[str] = mapped_column(BigInteger, nullable=True, sort_order=80)
    admin: Mapped[bool] = mapped_column(Boolean, sort_order=90, default=False)
    profile: Mapped['Profiles'] = relationship('Profiles', back_populates='user', lazy='joined')

    async def password_verify(self, password: typing.Password):
        """
        Checks the password, if the password is invalid an exception will be raised

        :param password: Password
        :type password: typing.Password

        :raises InternalServerException: Internal server error
        :raises BadRequestException: Bad request

        :return: Boolean
        :rtype: bool
        """
        return await password_hasher.verify(password_hash=self.password, password=password)


class Profiles(Base):
    __tablename__ = 'profiles'

    profile_id: Mapped[typing.ProfileID] = mapped_column(Integer, primary_key=True, autoincrement=True)
    user: Mapped[Users] = relationship('Users', back_populates='profile', lazy='joined')
    user_id: Mapped[typing.UserID] = mapped_column(
        Integer,
        ForeignKey('users.user_id', onupdate='CASCADE', ondelete='CASCADE'),
    )
    first_name: Mapped[str] = mapped_column(String(200), nullable=True)
    last_name: Mapped[str] = mapped_column(String(200), nullable=True)
    date_birth: Mapped[date] = mapped_column(Date, nullable=True)
    gender: Mapped[typing.Gender] = mapped_column(Enum(typing.Gender), nullable=True)
    language: Mapped[typing.Language] = mapped_column(Enum(typing.Language), default=typing.Language.EN)
    locate: Mapped[typing.Locate] = mapped_column(Enum(typing.Locate), default=typing.Locate.EN_US)
    timezone: Mapped[str] = mapped_column(String(200), default='UTC')

    async def set_locate(self, locate: typing.Locate):
        if result := re.match('^([a-z]+)', locate.value):
            language: typing.Language = typing.Language[result.group(0).upper()]
            self.language: typing.Language = language
            self.locate: typing.Locate = locate
            await self.save()


class Tokens(Base):
    __tablename__ = 'tokens'

    token_id: Mapped[typing.TokenID] = mapped_column(Uuid, primary_key=True, sort_order=10)

    user_id: Mapped[typing.UserID] = mapped_column(
        Integer,
        ForeignKey('users.user_id', onupdate='CASCADE', ondelete='CASCADE'),
        nullable=True,
        sort_order=30,
    )

    access_token: Mapped[str] = mapped_column(Text, sort_order=60)
    refresh_token: Mapped[str] = mapped_column(Text, sort_order=70)
    expires_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=True, sort_order=80)

    user: Mapped['Users'] = relationship('Users', foreign_keys=user_id, lazy='select')


class Sessions(Base):
    __tablename__ = 'sessions'

    session_id: Mapped[UUID] = mapped_column(Uuid, primary_key=True, sort_order=10)
    expires_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), sort_order=50)
    data: Mapped[dict] = mapped_column(JSON(), nullable=True, sort_order=60)
    user_id: Mapped[typing.UserID] = mapped_column(
        Integer,
        ForeignKey('users.user_id', onupdate='CASCADE', ondelete='CASCADE'),
        nullable=True,
        sort_order=70,
    )
    user: Mapped['Users'] = relationship('Users', foreign_keys=user_id, lazy='select')


# class Permissions(Base):
#     __tablename__ = 'permissions'
#     permission_id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
#     name: Mapped[str] = mapped_column(String(200))
#     slug: Mapped[str] = mapped_column(String(200), unique=True)

# class Applications(Base):
#     __tablename__ = 'applications'
#
#     application_id: Mapped[int] = mapped_column(Integer, primary_key=True, sort_order=10)
#     name: Mapped[str] = mapped_column(String, sort_order=50)
#     client_id: Mapped[str] = mapped_column(String(40), unique=True, sort_order=60)
#     client_secret: Mapped[str] = mapped_column(String(40), sort_order=70)
#     redirect_uri: Mapped[List['RedirectURI']] = relationship('RedirectURI', lazy='subquery')
#
#
# class RedirectURI(Base):
#     __tablename__ = 'redirect_uri'
#
#     redirect_uri_id: Mapped[int] = mapped_column(Integer, primary_key=True, sort_order=10)
#     uri: Mapped[str] = mapped_column(String, sort_order=50)
#
#     application_id: Mapped[int] = mapped_column(
#         Integer,
#         ForeignKey('applications.application_id', onupdate='CASCADE', ondelete='CASCADE'),
#         nullable=True,
#         sort_order=60,
#     )
#
#     application: Mapped['Applications'] = relationship(
#         'Applications',
#         foreign_keys=application_id,
#         lazy='joined',
#     )
