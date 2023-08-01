from asyncio import sleep

import pytest

from fastid.exceptions import JWTAudienceException, JWTSignatureExpiredException, NotFoundException
from fastid.services import session
from fastid.settings import settings


async def test_create(db_migrations):
    jwt_token = await session.create(audience='test_audience')
    assert jwt_token

    session_obj = await session.get(jwt_token=jwt_token, audience='test_audience')
    assert session_obj.aud == 'test_audience'
    assert session_obj.iss == settings.jwt_iss


async def test_expire_time(db_migrations):
    jwt_token = await session.create(audience='test_audience', expire_time_second=1)
    await sleep(1)

    with pytest.raises(JWTSignatureExpiredException):
        await session.get(jwt_token=jwt_token, audience='test_audience')


async def test_audience(db_migrations):
    jwt_token = await session.create(audience='test_audience', expire_time_second=1)

    with pytest.raises(JWTAudienceException):
        await session.get(jwt_token=jwt_token, audience='test_audience_fail')


async def test_fail_iss(db_migrations):
    jwt_token = await session.create(audience='test_audience', payload={'iss': 'iss'})
    assert jwt_token


async def test_payload(db_migrations):
    jwt_token = await session.create(audience='test_audience', payload={'hello': 'word'})
    assert jwt_token

    session_obj = await session.get(jwt_token=jwt_token, audience='test_audience')
    assert session_obj.payload.get('hello') == 'word'


async def test_session_obj_str(db_migrations):
    jwt_token = await session.create(audience='test_audience', payload={'hello': 'word'})
    assert jwt_token

    session_obj = await session.get(jwt_token=jwt_token, audience='test_audience')
    assert str(session_obj)


async def test_obj_not_found(db_migrations):
    jwt_token = await session.create(audience='test_audience', payload={'hello': 'word'})
    assert jwt_token

    await session.remove(jwt_token=jwt_token, audience='test_audience')

    with pytest.raises(NotFoundException):
        await session.get(jwt_token=jwt_token, audience='test_audience')
