import uuid
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo

import jwt
from jwt import PyJWTError

from .. import repositories, services, typing
from ..exceptions import BadRequestException, NotFoundException
from ..settings import settings
from ..trace import decorator_trace
from . import models


@decorator_trace(name='services.tokens.create')
async def create(*, user_id: typing.UserID, audience: str | None = None) -> models.Token:
    current_datetime = datetime.now(tz=ZoneInfo('UTC'))
    token_id = uuid.uuid4()

    payload = {
        'iss': settings.jwt_iss,
        'jti': str(token_id),
        'iat': current_datetime,
        'exp': current_datetime + timedelta(seconds=settings.jwt_access_token_lifetime),
    }

    if audience is not None:
        payload['aud'] = audience

    access_token = jwt.encode(
        payload=payload,
        key=settings.jwt_secret.get_secret_value(),
        algorithm=settings.jwt_algorithm.value,
    )

    payload['exp'] = current_datetime + timedelta(seconds=settings.jwt_refresh_token_lifetime)

    refresh_token = jwt.encode(
        payload=payload,
        key=settings.jwt_secret.get_secret_value(),
        algorithm=settings.jwt_algorithm.value,
    )

    await repositories.tokens.create(
        token_id=typing.TokenID(token_id),
        access_token=access_token,
        refresh_token=refresh_token,
        user_id=user_id,
        expires_at=current_datetime + timedelta(seconds=settings.jwt_access_token_lifetime),
    )
    return models.Token(
        access_token=access_token,
        refresh_token=refresh_token,
        expires_in=settings.jwt_access_token_lifetime,
        user_id=user_id,
        token_id=typing.TokenID(token_id),
    )


@decorator_trace(name='services.tokens.reload')
async def reload(*, refresh_token: str, audience: str | None = None) -> models.Token:
    token = await get(jwt_token=refresh_token, audience=audience)
    await repositories.tokens.delete_by_id(token_id=token.token_id)
    return await create(user_id=token.user_id, audience=audience)


@decorator_trace(name='services.tokens.get')
async def get(*, jwt_token: str, audience: str | None = None) -> models.Token:
    options = {}
    if audience is None:
        options['verify_aud'] = False

    try:
        data = jwt.decode(
            jwt=jwt_token,
            key=settings.jwt_secret.get_secret_value(),
            algorithms=[settings.jwt_algorithm.value],
            audience=audience,
            issuer=settings.jwt_iss,
            verify=True,
            options=options,
        )
    except PyJWTError as err:
        raise NotFoundException(
            message='Token not found',
            i18n='token_not_found',
            params={'error': str(err)},
        ) from err

    token = await repositories.tokens.get_by_id(token_id=typing.TokenID(uuid.UUID(data.get('jti'))))
    if token is None:
        raise NotFoundException(
            message='Token not found',
            i18n='token_not_found',
            params={},
        )

    return models.Token(
        access_token=token.access_token,
        refresh_token=token.refresh_token,
        expires_in=settings.jwt_access_token_lifetime,
        user_id=token.user_id,
        token_id=token.token_id,
    )


@decorator_trace(name='services.tokens.delete')
async def delete_by_id(*, token_id: typing.TokenID) -> None:
    await repositories.tokens.delete_by_id(token_id=token_id)


@decorator_trace(name='services.tokens.signin')
async def signin(*, email: typing.Email, password: typing.Password) -> models.Token | None:
    user = await services.users.get_by_email(email=email)

    if not user:
        raise BadRequestException(
            i18n='email_or_password_incorrect',
            params={'email': email},
            message='Email or password is incorrect',
        )

    try:
        await services.password_hasher.verify(password_hash=user.password, password=password)
    except BadRequestException as err:
        raise BadRequestException(i18n='email_or_password_incorrect', message='Email or password is incorrect') from err

    return await create(user_id=user.user_id, audience='internal')
