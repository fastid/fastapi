import os
from enum import Enum
from pathlib import Path
from typing import Literal

from pydantic import SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict


class LogLevel(str, Enum):
    """A class for determining logging levels"""

    debug: str = 'DEBUG'
    info: str = 'INFO'
    warning: str = 'WARNING'
    fatal: str = 'FATAL'


class Environment(str, Enum):
    """A class for determining environments"""

    development: str = 'DEVELOPMENT'
    testing: str = 'TESTING'
    production: str = 'PRODUCTION'


class OpentelemetryProcess(str, Enum):
    http: str = 'http'
    devnull: str = 'devnull'
    stdout: str = 'stdout'


class Settings(BaseSettings):
    app_name: str = 'FastID'

    base_dir: Path = Path(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    """ Path to working directory """

    log_name: str = app_name
    """Logger name"""

    log_level: LogLevel = LogLevel.info
    """ Logging level """

    environment: Environment = Environment.production
    """ Environment """

    # DB
    db_host: str = 'localhost'
    """Database host address as one of the following: an IP address or a domain name"""

    db_port: int = 5432
    """Port number to connect to at the server host"""

    db_user: str = 'user'
    """The name of the database role used for authentication."""

    db_password: SecretStr = SecretStr('password')
    """Password to be used for authentication."""

    db_database: str = 'database'
    """The name of the database to connect to."""

    db_schema: str = 'public'
    """The name of the schema to connect to."""

    db_pool_size: int = 10
    """ The size of the pool to be maintained, defaults to 10.
    This is the largest number of connections that will be kept persistently in the pool. """

    db_max_overflow: int = 5
    """ The maximum overflow size of the pool.
    When the number of checked-out connections reaches the size set in pool_size, additional
    connections will be returned up to this limit.
    When those additional connections are returned to the pool, they are disconnected and discarded.
    It follows then that the total number of simultaneous connections the pool will allow is pool_size + max_overflow,
    and the total number of “sleeping” connections the pool will allow is pool_size. max_overflow can be set to -1 to
    indicate no overflow limit; no limit will be placed on the total number of concurrent connections. Defaults to 5.
    """

    trusted_hosts: list[str] = ['*']
    """ Trusted hosts """

    cors_enable: bool = False
    cors_allow_origins: list[str] = ['*']
    cors_allow_credentials: bool = True
    cors_allow_headers: list[str] = []
    cors_allow_methods: list[
        Literal[
            'GET',
            'POST',
            'PUT',
            'PATCH',
            'DELETE',
            'OPTIONS',
            'CONNECT',
            'HEAD',
            'TRACE',
        ]
    ] = []

    opentelemetry_service_name: str = app_name

    opentelemetry_process: OpentelemetryProcess = OpentelemetryProcess.devnull

    opentelemetry_host: str = 'tempo'
    """Tempo host address as one of the following: an IP address or a domain name"""

    opentelemetry_port: int = 4317
    """Port number to connect to at the server host"""

    # Http client
    http_client_timeout: int = 30
    """HTTP defaults to including reasonable timeouts for all network operations, while Requests has no timeouts by
    default."""

    http_client_max_keepalive_connections: int = 5
    """ Number of allowable keep-alive connections """

    http_client_max_connections: int = 10
    """ Maximum number of allowable connections """

    recaptcha_enable: bool = True
    recaptcha_key: str = '6LeIxAcTAAAAAJcZVRqyHh71UMIEGNQ_MXjiZKhI'
    recaptcha_secret_key: str = '6LeIxAcTAAAAAGG-vFI1TnRWxMZNFuojJ4WifJWe'

    password_policy_max_length: int = 200
    password_policy_min_length: int = 5

    model_config = SettingsConfigDict(
        env_file=f'{base_dir}/.env',
        env_file_encoding='utf-8',
        extra='allow',
    )


settings = Settings()
