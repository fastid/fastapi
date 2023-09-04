from hashlib import sha256
from random import randint

from sqlalchemy import insert, select

from ..exceptions import ConflictException, NotFoundException
from . import db, schemes


async def create(*, name: str, redirect_uri: list[str]) -> str:
    """
    Create an application

    :param name: Name application
    :param redirect_uri: List uri

    """

    client_id = sha256(str(randint(1, 100000000)).encode('utf-8')).hexdigest()[:40]
    client_secret = sha256(str(randint(1, 100000000)).encode('utf-8')).hexdigest()[:40]

    if await check_exists(client_id=client_id):
        raise ConflictException(message='Client id is found')

    stmt_application = insert(schemes.Applications).values(name=name, client_id=client_id, client_secret=client_secret)
    async with db.async_session() as session:
        await session.begin()
        application_cursor = await session.execute(stmt_application)

        application_id = application_cursor.lastrowid

        for uri in redirect_uri:
            uri = uri.lower().strip()
            await session.execute(insert(schemes.RedirectURI).values(uri=uri, application_id=application_id))

        await session.commit()
    return client_id


async def get_by_client_id(*, client_id: str) -> schemes.Applications:
    """
    Get application by client ID

    :param client_id: Client ID
    """

    async with db.async_session() as session:
        stmt = select(schemes.Applications).where(schemes.Applications.client_id == client_id)
        application = await session.scalar(stmt)
        if application is None:
            raise NotFoundException(message='Application not found')

        return application


async def check_exists(*, client_id: str) -> bool:
    async with db.async_session() as session:
        stmt = select(schemes.Applications).where(schemes.Applications.client_id == client_id)
        application = await session.scalar(stmt)
        if application is None:
            return False
        return True
