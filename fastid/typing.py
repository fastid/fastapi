from typing import NewType
from uuid import UUID

from pydantic import EmailStr

UserID = NewType('UserID', int)
ProfileID = NewType('ProfileID', int)
Phone = NewType('Phone', int)
SessionID = NewType('SessionID', UUID)
Email = NewType('Email', EmailStr)
Password = NewType('Password', str)
