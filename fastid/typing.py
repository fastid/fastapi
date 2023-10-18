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
