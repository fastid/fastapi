import uuid
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo

import jwt

from .. import repositories, typing
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
    )


@decorator_trace(name='services.tokens.refresh')
async def refresh(*, refresh_token: str, audience: str | None = None) -> models.Token:
    data = jwt.decode(
        jwt=refresh_token,
        key=settings.jwt_secret.get_secret_value(),
        algorithms=[settings.jwt_algorithm.value],
        audience=audience,
        issuer=settings.jwt_iss,
        verify=True,
    )

    token = await repositories.tokens.get_by_id(token_id=typing.TokenID(uuid.UUID(data.get('jti'))))
    user_id = token.user_id
    await repositories.tokens.delete_by_id(token_id=typing.TokenID(token.token_id))
    return await create(user_id=user_id, audience=audience)
