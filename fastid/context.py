from contextvars import ContextVar

from . import typing

cxt_api_version: ContextVar[int] = ContextVar('api_version', default=0)
cxt_ip: ContextVar[str | None] = ContextVar('ip', default=None)
cxt_user_id: ContextVar[typing.UserID] = ContextVar('user_id')
