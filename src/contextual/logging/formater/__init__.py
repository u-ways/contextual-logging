from __future__ import annotations

import json
import logging
from typing import Any

from contextual.logging.formater.attributes import (
    DEFAULT_LOG_RECORD_ATTRIBUTES_TO_EXCLUDE,
    COMMON_LOG_RECORD_ATTRIBUTES,
    ERROR_LOG_RECORD_ATTRIBUTES,
)
from contextual.logging.model.error_log_record import ErrorLogRecord
from contextual.logging.model.common_log_record import CommonLogRecord

# noinspection PyProtectedMember
from contextual.logging.processor.error_log_processor import _ErrorLogProcessor

# noinspection PyProtectedMember
from contextual.logging.processor.common_log_processor import _CommonLogProcessor


class JsonFormatter(logging.Formatter):
    """
    A custom log formatter that serializes log records as JSON strings.

    This is a JSON-based formatter that filters out the default log record attributes, and
    enrich the log with extra attributes if present before serializing the log record. You
    can also safely pass private (i.e. starting with an underscore) attributes to the log
    record, as they will be filtered out.
    """

    _error_processor = _ErrorLogProcessor()
    _common_processor = _CommonLogProcessor()

    def format(self, record: logging.LogRecord) -> str:
        errors_record: ErrorLogRecord | None = self._error_processor.process(record.__dict__)
        common_record: CommonLogRecord = self._common_processor.process(record.__dict__)

        errors_attributes = errors_record.to_dict() if errors_record is not None else {}
        common_attributes = common_record.to_dict()

        other_extra_log_attributes: dict[str, Any] = {
            key: value
            for key, value in record.__dict__.items()
            if not key.startswith("_")
            and key not in DEFAULT_LOG_RECORD_ATTRIBUTES_TO_EXCLUDE
            and key not in COMMON_LOG_RECORD_ATTRIBUTES
            and key not in ERROR_LOG_RECORD_ATTRIBUTES
        }

        final_log_record: dict[str, Any] = {**errors_attributes, **common_attributes, **other_extra_log_attributes}

        return json.dumps(final_log_record)
