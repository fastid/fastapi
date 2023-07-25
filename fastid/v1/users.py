from fastapi import APIRouter
from starlette import status

from .. import typing
from . import schemes

router = APIRouter(tags=['Users'], prefix='/users')


@router.post(
    path='/invite/email/',
    summary='Create a user by a link invitation sent to an email address',
    name='create_user_by_invite_link_to_email',
)
async def create_user_invate_email(body: schemes.RequestCreateUserByEmail) -> dict:
    return {}


# @router.post(
#     path='/username/',
#     summary='Create a user by username',
#     name='create_user_by_username',
# )
# async def create_user(body: schemes.RequestCreateUserByUsername) -> dict:
#     return {}
