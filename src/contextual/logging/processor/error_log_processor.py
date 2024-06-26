from __future__ import annotations

import traceback
from typing import Dict, Any, Optional, override

from contextual.logging.model.error_log_record import ErrorLogRecord
from contextual.logging.processor import BaseLogProcessor


class _ErrorLogProcessor(BaseLogProcessor[ErrorLogRecord]):
    """
    ErrorLogProcessor is a class that processes the exception information from the log record.

    It's useful when logging with logger.exception(...) or logger.error(...) when an exception
    is raised as it will extract the exception type, message, and stack trace from the log record
    to enrich the log message with this information.
    """

    @override
    def process(self, kwargs: Dict[str, Any]) -> Optional[ErrorLogRecord]:
        exc_info: tuple | None = kwargs.get("exc_info", None)
        if exc_info is not None and len(exc_info) == 3:
            exc_class, exc_object, exc_traceback = exc_info
            error_log_record = ErrorLogRecord(
                exception_type=exc_class.__name__,
                exception_message=str(exc_object),
                exception_stack_trace="".join(traceback.format_exception(exc_class, exc_object, exc_traceback)),
            )
            return error_log_record
        else:
            return None
