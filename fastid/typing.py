import enum
import uuid
from typing import NewType

from pydantic import EmailStr

UserID = NewType('UserID', int)
ProfileID = NewType('ProfileID', int)
Phone = NewType('Phone', int)
Email = NewType('Email', EmailStr)
Password = NewType('Password', str)
TokenID = NewType('TokenID', uuid.UUID)
SessionID = NewType('SessionID', uuid.UUID)
Username = NewType('Username', str)


class Gender(enum.Enum):
    NONE = 'none'
    MALE = 'male'
    FEMALE = 'female'


class Language(enum.Enum):
    EN = 'en'
    RU = 'ru'


class Locate(enum.Enum):
    EN_US = 'en-us'
    EN_GB = 'en-gb'
    EN_AU = 'en-au'
    EN_IE = 'en-ie'
    EN_IL = 'en-il'
    EN_IN = 'en-in'
    EN_NZ = 'en-nz'
    EN_SG = 'en-sg'
    RU = 'ru'
