from datetime import date
from enum import Enum
from typing import Annotated, Any

from pydantic import BaseModel, Field, PlainValidator, AfterValidator, model_validator, field_validator
from pydantic_core.core_schema import ValidationInfo, FieldValidationInfo
from pydantic_extra_types.phone_numbers import PhoneNumber

from .. import typing
from ..settings import settings


class Gender(str, Enum):
    """A class for determining logging levels"""

    male: str = 'Male'
    female: str = 'Female'


class RequestCreateUserByEmail(BaseModel):
    email: typing.Email = Field(..., title='Email address', description='Email address', max_length=200)
    password: typing.Password = Field(
        ...,
        title='Password',
        description='Password',
        max_length=settings.password_policy_max_length,
        min_length=settings.password_policy_min_length,
    )

    if settings.recaptcha_enable:
        recaptcha_verify: str = Field(..., title='Recaptcha Verify', description='Recaptcha Verify')

    # first_name: str = Field(..., title='First name', description='First name', max_length=200)
    # last_name: str = Field(..., title='Last name', description='Last name', max_length=200)
    # date_birth: date = Field(None, title='Date birth', description='Date birth')
    # gender: Gender = Field(None, title='Gender', description='Gender')


# class RequestCreateUserByUsername(BaseModel):
#     username: str = Field(
#         ...,
#         title='Username',
#         description='Username',
#         min_length=1,
#         max_length=50,
#         examples=['username'],
#     )


class ResponseEmpty(BaseModel):
    pass
