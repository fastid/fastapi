from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from fastapi.responses import ORJSONResponse
from prometheus_fastapi_instrumentator import Instrumentator

from . import __version__, handlers, middlewares, v1
from .exceptions import exc_handlers
from .logger import logger
from .settings import Environment, settings


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Lifespan Events
    See - https://fastapi.tiangolo.com/advanced/events/

    :param app: FastAPI

    """
    logger.info('Startup FastID service', extra={'environment': settings.environment.lower()})
    yield


app = FastAPI(
    title=settings.app_name,
    description='Authorization and authentication service',
    default_response_class=ORJSONResponse,
    docs_url='/api/',
    redoc_url=None,
    openapi_url='/api/v1/openapi.json',
    version=__version__,
    debug=True if settings.environment.development == Environment.development else False,
    swagger_ui_parameters={
        'displayRequestDuration': True,
        'persistAuthorization': True,
    },
    lifespan=lifespan,
    license_info={
        'name': 'MIT',
        'url': 'https://github.com/fastid/fastapi/blob/main/LICENSE',
    },
    contact={'name': 'Github', 'url': 'https://github.com/fastid/'},
    exception_handlers=exc_handlers,
)

# Prometheus metrics
Instrumentator(excluded_handlers=['/healthcheck/', '/metrics']).instrument(
    app,
    metric_namespace=settings.app_name.lower(),
).expose(app, include_in_schema=False)

# Middlewares
app.add_middleware(
    TrustedHostMiddleware,
    allowed_hosts=settings.trusted_hosts.split(','),
)

if settings.cors_enable:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.cors_allow_origins.split(','),
        allow_credentials=settings.cors_allow_credentials,
        allow_methods=settings.cors_allow_methods.split(','),
        allow_headers=settings.cors_allow_headers.split(','),
        expose_headers=settings.cors_expose_headers.split(','),
    )

# App middleware
app.add_middleware(middlewares.Middleware)

app.include_router(handlers.healthcheck.router)
app.include_router(v1.config.router, prefix='/api/v1')
app.include_router(v1.admin.router, prefix='/api/v1')
app.include_router(v1.users.router, prefix='/api/v1')
