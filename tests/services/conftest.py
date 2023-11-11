from typing import AsyncGenerator

import pytest

from fastid import services, typing
from fastid.services import models


@pytest.fixture
async def user(db_migrations) -> AsyncGenerator[models.User, None]:
    user = await services.users.create(
        email=typing.Email('user@exmaple.com'),
        password=typing.Password('password'),
    )

    assert isinstance(user, models.User)

    assert user is not None
    assert user.user_id
    assert user.email == typing.Email('user@exmaple.com')
    assert user.password
    assert user.created_at
    assert user.updated_at

    assert user.profile

    assert user.profile.language == typing.Language.EN
    assert user.profile.locate == typing.Locate.EN_US
    assert user.profile.timezone == 'UTC'

    yield user
