from typing import Any, Callable, Coroutine, Type, TypeVar, Union

from fastapi import HTTPException, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import ORJSONResponse
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


class ConflictException(MainException):
    """Conflict object"""

    def __init__(self, message: str = 'Conflict object'):
        super().__init__(message=message, status_code=status.HTTP_400_BAD_REQUEST)
        self.error = message


class BadRequestException(MainException):
    """Bad Request"""

    def __init__(self, message: str = 'Bad Request'):
        super().__init__(message=message, status_code=status.HTTP_400_BAD_REQUEST)
        self.error = message


class RecaptchaVerifyFailException(MainException):
    """Recaptcha verify fail"""

    def __init__(self, message: str = 'Recaptcha verify fail'):
        super().__init__(message=message, status_code=status.HTTP_400_BAD_REQUEST)
        self.error = message


class JWTAudienceException(MainException):
    def __init__(self, message: str = "JWT Audience doesn't match"):
        super().__init__(message=message, status_code=status.HTTP_400_BAD_REQUEST)
        self.error = message


class JWTSignatureExpiredException(MainException):
    def __init__(self, message: str = 'JWT Signature has expired'):
        super().__init__(message=message, status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
        self.error = message


class InternalServerException(MainException):
    def __init__(self, message: str = 'Internal server error'):
        super().__init__(message=message, status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
        self.error = message


def exception(exc_type: ExceptionType):
    async def wrapper(
        request: Request,
        err: (
            RequestValidationError
            | NotFoundException
            | ConflictException
            | BadRequestException
            | RecaptchaVerifyFailException
            | JWTSignatureExpiredException
            | JWTAudienceException
            | InternalServerException
        ),
    ):
        if isinstance(err, RequestValidationError):
            errors: dict[str, str] = {}
            for error in err.errors():
                field = str(error['loc'][-1])
                type_err = error['type']
                ctx: dict | None = error.get('ctx')
                msg = error['msg']

                if type_err == 'missing' and field == 'email':
                    errors[field] = 'Required email field'
                elif type_err == 'enum' and field == 'grant_type':
                    errors[field] = 'Required grant_type field'
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
    ConflictException: exception(ConflictException),
    BadRequestException: exception(BadRequestException),
    RecaptchaVerifyFailException: exception(RecaptchaVerifyFailException),
    JWTAudienceException: exception(JWTAudienceException),
    JWTSignatureExpiredException: exception(JWTSignatureExpiredException),
    InternalServerException: exception(InternalServerException),
}
