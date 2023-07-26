from typing import Any, Callable, Coroutine, Type, TypeVar, Union

from fastapi import HTTPException, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import ORJSONResponse
from opentelemetry.trace import get_current_span
from starlette.requests import Request
from starlette.responses import Response

from .logger import logger

ExceptionType = TypeVar('ExceptionType')


class MainException(HTTPException):
    def __init__(self, message: str, status_code: int):
        super().__init__(status_code=status_code, detail=message)
        self.status_code = status_code
        self.message = message


class NotFoundException(MainException):
    """Not found object"""

    def __init__(self, message: str = 'Object not found'):
        super().__init__(message=message, status_code=status.HTTP_404_NOT_FOUND)
        self.error = message


def exception(exc_type: ExceptionType):
    async def wrapper(
        request: Request,
        err: (
            RequestValidationError |
            NotFoundException
        ),
    ):
        if isinstance(err, RequestValidationError):

            errors: dict[str, str] = {}
            for error in err.errors():  # pragma: no cover
                field = str(error['loc'][-1])
                type_err = error['type']
                ctx: dict | None = error.get('ctx')
                msg = error['msg']

                if type_err == 'missing' and field == 'email':
                    errors[field] = 'Required email field'
                else:
                    errors[field] = msg

                logger.debug('Error', extra={'field': field, 'type_err': type_err, 'ctx': ctx})
            return ORJSONResponse(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, content={'errors': errors})

        return ORJSONResponse(
            status_code=err.status_code,
            content={'error': err.message},
        )
    return wrapper


exc_handlers: dict[Union[int, Type[Exception]], Callable[[Request, Any], Coroutine[Any, Any, Response]]] | None = {
    RequestValidationError: exception(RequestValidationError),
    NotFoundException: exception(NotFoundException),
}
