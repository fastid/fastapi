import pytest
from fastapi import FastAPI

from fastid.exceptions import BadRequestException, ConflictException, NotFoundException, UnauthorizedException


async def test_exception_not_found(app: FastAPI):
    with pytest.raises(NotFoundException):
        raise NotFoundException


async def test_exception_conflict(app: FastAPI):
    with pytest.raises(ConflictException):
        raise ConflictException


async def test_exception_bad_request(app: FastAPI):
    with pytest.raises(BadRequestException):
        raise BadRequestException


async def test_exception_unauthorizedt(app: FastAPI):
    with pytest.raises(UnauthorizedException):
        raise UnauthorizedException
