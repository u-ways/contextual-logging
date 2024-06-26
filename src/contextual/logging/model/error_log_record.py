from dataclasses import dataclass
from typing import Dict, Any, override

from contextual.logging.model import BaseLogRecord


@dataclass
class ErrorLogRecord(BaseLogRecord):
    exception_type: str = ""
    exception_message: str = ""
    exception_stack_trace: str = ""

    @override
    def to_dict(self) -> Dict[str, Any]:
        return {"error": super().to_dict()}
