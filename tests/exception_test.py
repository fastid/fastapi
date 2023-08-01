import pytest
from fastapi import FastAPI

from fastid.exceptions import NotFoundException


async def test_exception_not_found(app: FastAPI):
    with pytest.raises(NotFoundException):
        raise NotFoundException
