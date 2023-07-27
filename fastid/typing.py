from typing import NewType

from pydantic import EmailStr

UserID = NewType('UserID', int)
ProfileID = NewType('ProfileID', int)
Phone = NewType('Phone', int)
SessionID = NewType('SessionID', int)
Email = NewType('Email', EmailStr)
Password = NewType('Password', str)
