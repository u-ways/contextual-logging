from dataclasses import fields

from contextual.logging.model.error_log_record import ErrorLogRecord
from contextual.logging.model.http_log_record import HttpLogRecord
from contextual.logging.model.common_log_record import CommonLogRecord

"""
Uniquely identifies every request involved in operation processing,
and is generated on the caller side and passed to callee.

Within HTTP headers, this is usually set as `x-request-id`.
"""
REQUEST_ID_ATTRIBUTE: str = "request_id"

"""
Also known as a Transit ID, is a unique identifier value that is attached to requests
and messages that allow reference to a particular transaction or event chain.

For Correlation ID, in general, you don’t have to use one. But if you are designing a
distributed system that incorporates message queues and asynchronous processing, you will
do well to include a Correlation ID in your messages.

Within HTTP headers, this is usually set as `x-correlation-id`.
"""
TRACEABILITY_ID_ATTRIBUTE: str = "correlation_id"

"""
A set containing the standard LogRecord attributes that the Python logger enriches log messages with
by default. In our case, this set is used to filter out these attributes from the log message before
serializing the log message as we use custom attributes instead.

See: https://docs.python.org/3/library/logging.html#logrecord-attributes
"""
DEFAULT_LOG_RECORD_ATTRIBUTES_TO_EXCLUDE: set[str] = {
    "args",
    "asctime",
    "created",
    "exc_info",
    "exc_text",
    "filename",
    "funcName",
    "levelname",
    "levelno",
    "lineno",
    "module",
    "msecs",
    "msg",
    "name",
    "pathname",
    "process",
    "processName",
    "relativeCreated",
    "stack_info",
    "thread",
    "threadName",
    "taskName",
}

"""
A set containing any optional log record attributes that can be included in log messages.
If you have more optional attributes that don't fit into a certain category, you can add them here.
"""
OPTIONAL_LOG_RECORD_ATTRIBUTES: set[str] = {
    "message",
}

COMMON_LOG_RECORD_ATTRIBUTES: set[str] = {field.name for field in fields(CommonLogRecord)}

HTTP_LOG_RECORD_ATTRIBUTES: set[str] = {field.name for field in fields(HttpLogRecord)}

ERROR_LOG_RECORD_ATTRIBUTES: set[str] = {field.name for field in fields(ErrorLogRecord)}
