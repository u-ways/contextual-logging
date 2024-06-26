from dataclasses import dataclass

from contextual.logging.model import BaseLogRecord


@dataclass
class CommonLogRecord(BaseLogRecord):
    application_name: str = ""
    timestamp: str = ""
    log_level: str = ""
