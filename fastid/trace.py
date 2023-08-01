import os
from collections.abc import Callable, Coroutine
from functools import wraps
from typing import Any, ParamSpec, TypeVar

from opentelemetry import trace
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor, ConsoleSpanExporter

from .settings import OpentelemetryProcess, settings

P = ParamSpec('P')
T = TypeVar('T')


resource = Resource(attributes={'service.name': settings.opentelemetry_service_name})

trace.set_tracer_provider(TracerProvider(resource=resource))
tracer_provider: TracerProvider = trace.get_tracer_provider()  # type: ignore

if settings.opentelemetry_process == OpentelemetryProcess.devnull:
    processor = BatchSpanProcessor(ConsoleSpanExporter(out=open(os.devnull, 'w')))
elif settings.opentelemetry_process == OpentelemetryProcess.stdout:  # pragma: no cover
    processor = BatchSpanProcessor(ConsoleSpanExporter())
else:  # pragma: no cover
    processor = BatchSpanProcessor(
        OTLPSpanExporter(
            endpoint=f'http://{settings.opentelemetry_host}:{settings.opentelemetry_port}',
        ),
    )

tracer_provider.add_span_processor(processor)


def decorator_trace(name: str = 'n/a'):
    """
    Decorator for the function, supports asynchronous functions,
    allows you to create a span inside the parent
        Example:
        .. code-block:: python
            @decorator_trace()
    """

    def decorator(function: Callable[P, Coroutine[Any, Any, T]]) -> Callable[P, Coroutine[Any, Any, T]]:
        @wraps(function)
        async def wrapper(*args: P.args, **kwargs: P.kwargs) -> T:
            with trace.get_tracer(settings.opentelemetry_service_name).start_as_current_span(name):
                return await function(*args, **kwargs)

        return wrapper

    return decorator
