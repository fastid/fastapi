from fastapi import APIRouter
from starlette import status

from .. import typing
from ..exceptions import NotFoundException
from . import schemes

router = APIRouter(tags=['Users'], prefix='/users')


@router.post(
    path='/email/',
    summary='Create a user by email address',
    name='create_user_by_email_address',
)
async def create_user_by_email(body: schemes.RequestCreateUserByEmail) -> schemes.ResponseEmpty:
    return schemes.ResponseEmpty()
