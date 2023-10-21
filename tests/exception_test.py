import pytest
from fastapi import FastAPI

from fastid.exceptions import ConflictException, NotFoundException


async def test_exception_not_found(app: FastAPI):
    with pytest.raises(NotFoundException):
        raise NotFoundException


async def test_exception_conflict(app: FastAPI):
    with pytest.raises(ConflictException):
        raise ConflictException
