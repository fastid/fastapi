from typing import Any, Callable, Coroutine, Type, TypeVar, Union

from fastapi import HTTPException, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import ORJSONResponse
from pydantic import BaseModel
from starlette.requests import Request
from starlette.responses import Response

from .logger import logger

ExceptionType = TypeVar('ExceptionType')


class ModelI18nException(BaseModel):
    message: str
    params: dict


class ModelMessageException(BaseModel):
    message: str
    i18n: ModelI18nException


class ModelException(BaseModel):
    error: ModelMessageException
    errors: dict[str, ModelMessageException]


class MainException(HTTPException):
    def __init__(self, message: str, status_code: int, i18n: str | None = None, params: dict | None = None):
        super().__init__(status_code=status_code, detail=message)
        self.status_code = status_code
        self.message = message
        self.i18n = i18n
        self.params = params if params else {}


class NotFoundException(MainException):
    """Not found object"""

    def __init__(self, message: str = 'Object not found', i18n: str | None = None, params: dict | None = None):
        super().__init__(message=message, status_code=status.HTTP_404_NOT_FOUND, i18n=i18n, params=params)
        self.error = message


class ConflictException(MainException):
    """Conflict object"""

    def __init__(self, message: str = 'Conflict object', i18n: str | None = None, params: dict | None = None):
        super().__init__(message=message, status_code=status.HTTP_400_BAD_REQUEST, i18n=i18n, params=params)
        self.error = message


class UnauthorizedException(MainException):
    """Unauthorized object"""

    def __init__(self, message: str = 'Unauthorized object', i18n: str | None = None, params: dict | None = None):
        super().__init__(message=message, status_code=status.HTTP_401_UNAUTHORIZED, i18n=i18n, params=params)
        self.error = message


class BadRequestException(MainException):
    """Bad Request"""

    def __init__(self, message: str = 'Bad Request', i18n: str | None = None, params: dict | None = None):
        super().__init__(message=message, status_code=status.HTTP_400_BAD_REQUEST, i18n=i18n, params=params)
        self.error = message


class RecaptchaVerifyFailException(MainException):
    """Recaptcha verify fail"""

    def __init__(self, message: str = 'Recaptcha verify fail', i18n: str | None = None, params: dict | None = None):
        super().__init__(message=message, status_code=status.HTTP_400_BAD_REQUEST, i18n=i18n, params=params)
        self.error = message


class JWTAudienceException(MainException):
    def __init__(
        self,
        message: str = "JWT Audience doesn't match",
        i18n: str | None = None,
        params: dict | None = None,
    ):
        super().__init__(message=message, status_code=status.HTTP_400_BAD_REQUEST, i18n=i18n, params=params)
        self.error = message


class JWTSignatureExpiredException(MainException):
    def __init__(self, message: str = 'JWT Signature has expired', i18n: str | None = None, params: dict | None = None):
        super().__init__(message=message, status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, i18n=i18n, params=params)
        self.error = message


class InternalServerException(MainException):
    def __init__(self, message: str = 'Internal server error', i18n: str | None = None, params: dict | None = None):
        super().__init__(message=message, status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, i18n=i18n, params=params)
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
            | UnauthorizedException
            | InternalServerException
        ),
    ):
        if isinstance(err, RequestValidationError):  # pragma: no cover
            errors: dict[str, dict] = {}
            for error in err.errors():
                field = str(error['loc'][-1])
                type_err = error['type']
                input_ = error['input']
                ctx: dict | None = error.get('ctx')
                msg = error['msg']

                logger.debug('Error', extra={'field': field, 'type_err': type_err, 'input': input_, 'ctx': ctx})

                if type_err == 'missing':
                    errors[field] = {
                        'message': f'The field {field} is not filled',
                        'i18n': {
                            'message': 'field_not_filled',
                            'params': {'field': field},
                        },
                    }
                elif type_err == 'value_error' and field == 'email':
                    errors[field] = {
                        'message': 'Incorrect email address',
                        'i18n': {
                            'message': 'incorrect_email_address',
                            'params': {'email': input_},
                        },
                    }
                elif type_err in ['string_too_short', 'string_too_long']:
                    errors[field] = {
                        'message': msg,
                        'i18n': {
                            'message': type_err,
                            'params': ctx,
                        },
                    }
                else:
                    errors[field] = {
                        'message': msg,
                        'i18n': {
                            'message': 'unknown_error',
                            'params': {},
                        },
                    }
            return ORJSONResponse(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, content={'errors': errors})

        return ORJSONResponse(
            status_code=err.status_code,
            content={
                'error': {
                    'message': err.message,
                    'i18n': {
                        'message': err.i18n if err.i18n else 'unknown_error',
                        'params': err.params,
                    },
                },
            },
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
    UnauthorizedException: exception(UnauthorizedException),
    InternalServerException: exception(InternalServerException),
}

exception_responses: dict[int | str, dict[str, Any]] | None = {
    404: {'model': ModelException},
    403: {'model': ModelException},
    401: {'model': ModelException},
    409: {'model': ModelException},
    400: {'model': ModelException},
    422: {'model': ModelException},
    500: {'model': ModelException},
}
