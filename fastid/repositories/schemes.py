from datetime import datetime

from sqlalchemy import JSON, BigInteger, DateTime, ForeignKey, Integer, String, func
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship

from ..typing import Email, Phone, ProfileID, SessionID, UserID


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
    username: Mapped[str] = mapped_column(String(200), unique=True, nullable=True, sort_order=50)
    email: Mapped[Email] = mapped_column(String(200), unique=True, nullable=True, sort_order=60)
    password: Mapped[str] = mapped_column(String(200), nullable=True, sort_order=70)

    # profile: Mapped['Profiles'] = relationship('Profiles', back_populates='user', lazy='joined')


# class Profiles(Base):
#     __tablename__ = 'profiles'
#
#     profile_id: Mapped[ProfileID] = mapped_column(Integer, primary_key=True, autoincrement=True)
#     user: Mapped[Users] = relationship('Users', back_populates='profile', lazy='joined')
#     user_id: Mapped[UserID] = mapped_column(
#         Integer,
#         ForeignKey('users.user_id', onupdate='CASCADE', ondelete='CASCADE'),
#     )
#     email: Mapped[Email] = mapped_column(String(100), unique=True, nullable=True)
#     phone: Mapped[Phone] = mapped_column(BigInteger, unique=True, nullable=True)


class Sessions(Base):
    __tablename__ = 'sessions'

    session_id: Mapped[SessionID] = mapped_column(Integer, primary_key=True, autoincrement=True)
    expire_at: Mapped[datetime] = mapped_column(DateTime(timezone=True))
    data: Mapped[dict] = mapped_column(JSON(), nullable=True)
    user_id: Mapped[UserID] = mapped_column(
        Integer,
        ForeignKey('users.user_id', onupdate='CASCADE', ondelete='CASCADE'),
        nullable=True,
    )
    user: Mapped['Users'] = relationship('Users', foreign_keys=user_id, lazy='select')
