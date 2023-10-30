import asyncclick as click

from .. import services


def abort_if_false(ctx, param, value):
    if not value:
        ctx.abort()


@click.command()
@click.option(
    '--email',
    prompt='Enter the email address',
    help='Email address',
)
@click.option(
    '--password',
    prompt='Your password',
    hide_input=True,
    confirmation_prompt=True,
    help='Password',
)
@click.option(
    '--yes',
    is_flag=True,
    callback=abort_if_false,
    expose_value=False,
    prompt='Are you sure you want to create user?',
)
async def create_admin(email, password):
    if await services.users.get_by_email(email=email):
        click.echo('The user already exists!')
        return

    result = await services.users.create(email=email, password=password)
    if result:
        click.echo('User successfully created!')
