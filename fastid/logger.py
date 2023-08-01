import logging
import sys
from contextvars import ContextVar

from opentelemetry.trace import get_current_span
from pythonjsonlogger import jsonlogger

from .settings import settings

cxt_request_id: ContextVar[str | None] = ContextVar('request_id', default=None)

__all__ = ['logger', 'cxt_request_id']


class CustomJsonFormatter(jsonlogger.JsonFormatter):
    def add_fields(self, log_record, record, message_dict):
        super().add_fields(log_record, record, message_dict)

        log_record['level'] = record.levelname
        log_record['module'] = f'{record.module}:{record.funcName}({record.lineno})'
        log_record['pathname'] = record.pathname

        if request_id := cxt_request_id.get():
            log_record['request_id'] = request_id

        current_span = get_current_span()
        if not current_span.get_span_context().trace_id == 0:
            log_record['span_id'] = format(current_span.get_span_context().span_id, '016x')
            log_record['trace_id'] = format(current_span.get_span_context().trace_id, '032x')


class InfoFilter(logging.Filter):
    def filter(self, rec):  # noqa: A003
        return rec.levelno in (logging.DEBUG, logging.INFO)


__formatter = CustomJsonFormatter()

# StreamHandler
__handler_stream_stdout = logging.StreamHandler(sys.stdout)
__handler_stream_stderr = logging.StreamHandler(sys.stderr)

__handler_stream_stdout.setLevel(logging.DEBUG)
__handler_stream_stderr.setLevel(logging.WARNING)

__handler_stream_stdout.setFormatter(__formatter)
__handler_stream_stderr.setFormatter(__formatter)

__handler_stream_stdout.addFilter(InfoFilter())

__log = logging.getLogger(settings.log_name)
__log.setLevel(settings.log_level.upper())
__log.addHandler(__handler_stream_stdout)
__log.addHandler(__handler_stream_stderr)

logger = logging.getLogger(settings.log_name)
