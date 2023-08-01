import uuid
from datetime import datetime, timedelta
from typing import Union
from zoneinfo import ZoneInfo

import jwt
from jwt import ExpiredSignatureError, InvalidAudienceError

from .. import repositories
from ..exceptions import JWTAudienceException, JWTSignatureExpiredException
from ..settings import JWTAlgorithm, settings
from ..trace import decorator_trace


class Session:
    def __init__(
        self,
        *,
        iss: str,
        jti: uuid.UUID,
        jwt_token: str,
        iat: datetime,
        exp: datetime,
        aud: str,
        payload: dict,
        data: dict,
    ):
        self.iss = iss
        self.jti = jti
        self.jwt_token = jwt_token
        self.iat = iat
        self.exp = exp
        self.aud = aud
        self.payload = payload
        self.data = data

    def __str__(self):
        return f'Session(iss:{self.iss}, jti:{self.jti}, iat:{self.iat}, exp:{self.exp}, aud:{self.aud})'


@decorator_trace(name='services.session.create')
async def create(
    audience: str,
    expire_time_second: int = 60 * 60 * 24,
    payload: dict[str, Union[bool, str, int]] | None = None,
    data: dict[str, Union[bool, str, int]] | None = None,
) -> str:
    """
    Creates a jwt token

    :param audience: String  that identifies the recipients that the JWT is intended for
    :param expire_time_second: Token lifetime
    :param payload: Payload jwt token
    :param data: Parameters that will not be available in the jwt token, but will be written to the database
    :return:
    """

    expire_at = datetime.now(tz=ZoneInfo('UTC')) + timedelta(seconds=expire_time_second)
    session_id = uuid.uuid4()
    iat = datetime.now(tz=ZoneInfo('UTC'))

    # We delete the keys that form the jwt token
    if payload:
        for key in ['iss', 'jti', 'iat', 'exp', 'aud']:
            if payload.get(key):
                del payload[key]
    else:
        payload = {}

    jwt_token = jwt.encode(
        payload={
            **payload,
            'iss': settings.jwt_iss,
            'jti': str(session_id),
            'iat': iat,
            'exp': expire_at,
            'aud': audience,
        },
        key=settings.jwt_secret.get_secret_value(),
        algorithm=settings.jwt_algorithm.value,
    )

    # We write it to the database
    await repositories.session.create(session_id=session_id, expire_at=expire_at, data=data)

    return jwt_token


@decorator_trace(name='services.session.get')
async def get(jwt_token: str, audience: str) -> Session:
    try:
        data: dict = jwt.decode(
            jwt=jwt_token,
            key=settings.jwt_secret.get_secret_value(),
            algorithms=JWTAlgorithm.get_all(),
            audience=audience,
        )
    except InvalidAudienceError as e:
        raise JWTAudienceException from e
    except ExpiredSignatureError as e:
        raise JWTSignatureExpiredException from e
    else:
        payload = {}

        for key, val in data.items():
            if key not in ['iss', 'jti', 'exp', 'aud', 'iat']:
                payload[key] = val

        session_obj = await repositories.session.get(session_id=uuid.UUID(data.get('jti')))

        return Session(
            iss=str(data.get('iss')),
            jti=uuid.UUID(data.get('jti')),
            jwt_token=jwt_token,
            exp=datetime.fromtimestamp(float(data.get('exp', 0)), tz=ZoneInfo('UTC')),
            aud=str(data.get('aud')),
            iat=datetime.fromtimestamp(float(data.get('iat', 0)), tz=ZoneInfo('UTC')),
            payload=payload,
            data=session_obj.data if session_obj else {},
        )


@decorator_trace(name='services.session.remove')
async def remove(jwt_token: str, audience: str) -> None:
    session_obj = await get(jwt_token=jwt_token, audience=audience)
    await repositories.session.remove(session_id=uuid.UUID(str(session_obj.jti)))
