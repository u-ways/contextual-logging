import time
from datetime import datetime, timezone
from typing import Dict, Any, override

from contextual.logging.model.common_log_record import CommonLogRecord
from contextual.logging.processor import BaseLogProcessor


class _CommonLogProcessor(BaseLogProcessor[CommonLogRecord]):
    """
    CommonLogProcessor is a class that processes the standard log record attributes
    that we except to be present in all log messages. (e.g. log level, timestamp, ...etc.)

    If any of the common attributes are missing, an exception is raised with a descriptive message.
    This enforces the developer to correctly configure the contextual logger with the required
    attributes.
    """

    @override
    def process(self, kwargs: Dict[str, Any]) -> CommonLogRecord:
        application_name_attribute = self.extract_attribute(kwargs, "application_name")
        log_level_attribute = self.extract_attribute(kwargs, "levelname")

        timestamp_attribute = datetime.fromtimestamp(
            float(kwargs.get("created", time.time())), tz=timezone.utc
        ).isoformat(timespec="microseconds")

        return CommonLogRecord(
            application_name=application_name_attribute,
            timestamp=timestamp_attribute,
            log_level=log_level_attribute,
        )
