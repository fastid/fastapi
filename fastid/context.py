from contextvars import ContextVar

cxt_api_version: ContextVar[int] = ContextVar('api_version', default=0)
cxt_ip: ContextVar[str | None] = ContextVar('ip', default=None)
