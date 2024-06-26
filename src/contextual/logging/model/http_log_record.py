from dataclasses import dataclass
from typing import Dict, Any, override

from contextual.logging.model import BaseLogRecord


@dataclass
class HttpLogRecord(BaseLogRecord):
    request_id: str = ""
    request_method: str = ""
    request_url: str = ""
    request_query_params: Dict[str, Any] = None
    request_headers: Dict[str, Any] = None
    response_status: int = 0
    response_headers: Dict[str, Any] = None
    response_duration_ms: float = 0.0

    @override
    def to_dict(self) -> Dict[str, Any]:
        return {"http": super().to_dict()}
