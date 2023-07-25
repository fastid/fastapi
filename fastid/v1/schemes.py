from pydantic import BaseModel, Field
from pydantic_extra_types.phone_numbers import PhoneNumber

from .. import typing


class RequestCreateUserByEmail(BaseModel):
    email: typing.Email = Field(..., title='Email address', description='Email address', max_length=200)


# class RequestCreateUserByUsername(BaseModel):
#     username: str = Field(
#         ...,
#         title='Username',
#         description='Username',
#         min_length=1,
#         max_length=50,
#         examples=['username'],
#     )
