from datetime import datetime
from uuid import UUID

from sqlalchemy import JSON, DateTime, ForeignKey, Integer, String, Text, Uuid, func
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship

from ..typing import Email, TokenID, UserID


class Base(DeclarativeBase):
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


class Users(Base):
    __tablename__ = 'users'

    user_id: Mapped[UserID] = mapped_column(Integer, primary_key=True, autoincrement=True, sort_order=10)
    email: Mapped[Email] = mapped_column(String(200), unique=True, nullable=True, sort_order=60)
    password: Mapped[str] = mapped_column(String(200), nullable=True, sort_order=70)

    # profile: Mapped['Profiles'] = relationship('Profiles', back_populates='user', lazy='joined')


class Tokens(Base):
    __tablename__ = 'tokens'

    token_id: Mapped[TokenID] = mapped_column(Uuid, primary_key=True, sort_order=10)

    user_id: Mapped[UserID] = mapped_column(
        Integer,
        ForeignKey('users.user_id', onupdate='CASCADE', ondelete='CASCADE'),
        nullable=True,
        sort_order=30,
    )

    access_token: Mapped[str] = mapped_column(Text, sort_order=60)
    refresh_token: Mapped[str] = mapped_column(Text, sort_order=70)
    expires_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=True, sort_order=80)

    user: Mapped['Users'] = relationship('Users', foreign_keys=user_id, lazy='select')


# class Profiles(Base):
#     __tablename__ = 'profiles'
#
#     profile_id: Mapped[ProfileID] = mapped_column(Integer, primary_key=True, autoincrement=True)
#     user: Mapped[Users] = relationship('Users', back_populates='profile', lazy='joined')
#     user_id: Mapped[UserID] = mapped_column(
#         Integer,
#         ForeignKey('users.user_id', onupdate='CASCADE', ondelete='CASCADE'),
#     )
#     first_name: Mapped[str] = mapped_column(String(200), unique=True, nullable=True)
#     last_name: Mapped[str] = mapped_column(String(200), unique=True, nullable=True)


class Sessions(Base):
    __tablename__ = 'sessions'

    session_id: Mapped[UUID] = mapped_column(Uuid, primary_key=True, sort_order=10)
    expires_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), sort_order=50)
    data: Mapped[dict] = mapped_column(JSON(), nullable=True, sort_order=60)
    user_id: Mapped[UserID] = mapped_column(
        Integer,
        ForeignKey('users.user_id', onupdate='CASCADE', ondelete='CASCADE'),
        nullable=True,
        sort_order=70,
    )
    user: Mapped['Users'] = relationship('Users', foreign_keys=user_id, lazy='select')


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
