import os
import time
import traceback
from uuid import uuid4

from fastapi import Request, status
from fastapi.responses import ORJSONResponse
from opentelemetry.semconv.trace import SpanAttributes
from opentelemetry.trace import Status, StatusCode
from starlette.datastructures import Headers, MutableHeaders
from starlette.types import ASGIApp, Message, Receive, Scope, Send

from .context import cxt_api_version, cxt_ip
from .logger import cxt_request_id, logger
from .settings import Environment, settings
from .trace import trace


class Middleware:
    def __init__(self, app: ASGIApp):
        self.app = app

    async def __call__(self, scope: Scope, receive: Receive, send: Send) -> None:
        # Timer
        start_timer = time.monotonic()

        if scope['type'] not in ('http',):  # pragma: no cover
            await self.app(scope, receive, send)
            return

        request = Request(scope=scope)

        cxt_ip_token = cxt_ip.set('127.0.0.1')
        cxt_request_id_token = cxt_request_id.set(request.headers.get('request-id', str(uuid4())))

        # IP
        if ip := request.headers.get('x-real-ip', request.headers.get('x-forwarded-for')):
            cxt_ip_token = cxt_ip.set(ip)

        # API Version
        ctx_api_version_token = cxt_api_version.set(0)
        if 'v1' in request.url.path.split('/', 3):
            ctx_api_version_token = cxt_api_version.set(1)

        path = request.scope.get('path')
        method = request.scope.get('method')

        with trace.get_tracer(settings.opentelemetry_service_name).start_as_current_span(f'{method} {path}') as span:
            span.set_attributes(
                {
                    SpanAttributes.HTTP_SCHEME: request.scope.get('scheme', 'n/a'),
                    SpanAttributes.HTTP_URL: request.url.path,
                    SpanAttributes.HTTP_CLIENT_IP: cxt_ip.get() or '0.0.0.0',
                    SpanAttributes.HTTP_USER_AGENT: request.headers.get('user-agent', 'n/a'),
                    SpanAttributes.HTTP_METHOD: request.method,
                    'request_id': cxt_request_id.get() or '',
                },
            )

            if cxt_api_version.get() > 0:
                span.set_attribute('api.version', cxt_api_version.get())

            async def send_wrapper(message: Message) -> None:
                if message['type'] == 'http.response.start':
                    headers_req = Headers(raw=message.get('headers'))

                    headers = MutableHeaders(scope=message)

                    # Adding the header Request-ID server response
                    headers.append('Request-Id', cxt_request_id.get() or '')

                    # Adding the header Trace-ID server response
                    if not span.get_span_context().trace_id == 0:
                        headers.append('Trace-Id', format(span.get_span_context().trace_id, '032x'))

                    span.set_attributes(
                        {
                            SpanAttributes.HTTP_STATUS_CODE: int(message.get('status', 0)),
                            SpanAttributes.HTTP_RESPONSE_CONTENT_LENGTH: int(headers_req.get('content-length', 0)),
                        },
                    )

                await send(message)

            extra = {
                'method': request.method,
                'user-agent': request.headers.get('user-agent', 'n/a'),
                'ip': cxt_ip.get() or '0.0.0.0',
                'uri': request.url.path,
                'request_duration_seconds': round(time.monotonic() - start_timer, 3),
            }

            try:
                await self.app(scope, receive, send_wrapper)
            except Exception as exc:
                if settings.environment == Environment.development and not os.environ.get('PYTEST'):  # pragma: no cover
                    traceback.print_exc()

                response = ORJSONResponse(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    content={'error': 'Internal server error'},
                )

                extra['exception.message'] = f'{exc}'

                if settings.environment != Environment.development:  # pragma: no cover
                    logger.error(msg=f'{request.method} {request.url.path}', extra=extra)

                span.record_exception(exception=exc)
                span.set_status(Status(status_code=StatusCode.ERROR, description=f'{exc}'))

                # Reset context var
                cxt_ip.reset(cxt_ip_token)
                cxt_api_version.reset(ctx_api_version_token)
                cxt_request_id.reset(cxt_request_id_token)

                await response(scope, receive, send_wrapper)
                return

            span.set_status(Status(status_code=StatusCode.OK))

            if request.url.path not in ['/metrics', '/healthcheck/']:
                logger.info(msg=f'{request.method} {request.url.path}', extra=extra)

            # Reset context var
            cxt_ip.reset(cxt_ip_token)
            cxt_api_version.reset(ctx_api_version_token)
            cxt_request_id.reset(cxt_request_id_token)
