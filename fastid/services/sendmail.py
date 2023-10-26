from email import utils
from email.mime.text import MIMEText

from aiosmtplib import SMTP
from jinja2 import Environment as Jinja2Environment
from jinja2 import FileSystemLoader
from opentelemetry.trace import get_current_span

from .. import typing
from ..logger import logger
from ..settings import Environment, settings
from ..trace import decorator_trace


@decorator_trace(name='services.sendmail.send')
async def send(
    email: typing.Email,
    template: str,
    subject: str,
    params: dict,
    name: str | None = None,
) -> None:
    span = get_current_span()

    env = Jinja2Environment(
        loader=FileSystemLoader(f'{settings.base_dir}/fastid/templates/email/'),
        enable_async=True,
        autoescape=True,
    )
    tmpl = env.get_template(template)

    params['app_name'] = settings.app_name

    body = await tmpl.render_async(params)

    msg = MIMEText(body, _subtype='html', _charset='utf-8')
    msg['Subject'] = subject
    msg['Message-ID'] = utils.make_msgid(domain=settings.mime_domain, idstring=settings.mime_idstring)
    msg['Date'] = utils.formatdate(localtime=False)
    msg['From'] = utils.formataddr((settings.default_email_name, settings.default_email))

    if name:
        msg['To'] = utils.formataddr((name, email))
    else:
        msg['To'] = email

    smtp = SMTP(
        hostname=settings.smtp_host,
        port=settings.smtp_port,
        validate_certs=False,
        use_tls=True if settings.environment == Environment.production else False,
        username=settings.smtp_username,
        password=settings.smtp_password.get_secret_value() if settings.smtp_password else None,
    )

    await smtp.connect()

    (_, status) = await smtp.sendmail(settings.default_email, email, msg.as_string())

    span.set_attributes(
        {
            'status': status,
            'template': template,
            'use_tls': True if settings.environment == Environment.production else False,
        },
    )

    logger.info(f'send mail status:{status}', extra={'status': status})
    await smtp.quit()
