from asyncclick.testing import CliRunner

from fastid import command

runner = CliRunner()


async def test_user(db_migrations):
    result = await runner.invoke(
        cli=command.user.create,
        args=['--email=user@exmaple.com', '--password=Qazwsx12345', '--yes', '--admin'],
    )
    assert result.output == 'User successfully created!\n'
    assert result.exit_code == 0

    result2 = await runner.invoke(
        cli=command.user.create,
        args=['--email=user@exmaple.com', '--password=Qazwsx12345', '--yes', '--admin'],
    )
    assert result2.output == 'The user already exists!\n'
    assert result2.exit_code == 0


async def test_create_admin_no(db_migrations):
    result = await runner.invoke(
        cli=command.user.create,
        args=['--email=user@exmaple.com', '--password=Qazwsx12345', '--admin'],
    )
    assert result.exit_code == 1
