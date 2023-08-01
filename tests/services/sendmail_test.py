from fastid import services, typing


async def test_send(mock_aiosmtplib):
    await services.sendmail.send(
        email=typing.Email('kostya@yandex.ru'),
        subject='Test subject',
        template='signup.html',
        params={'code': 1234},
    )

    await services.sendmail.send(
        name='User',
        email=typing.Email('user@exmaple.org'),
        subject='Test subject',
        template='signup.html',
        params={},
    )
