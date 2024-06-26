from dataclasses import dataclass, asdict
from typing import Dict

from contextual.logging.hinting import Primitive


@dataclass
class BaseLogRecord:
    """
    A base class for all custom log record extensions.
    """

    def to_dict(self) -> Dict[str, Primitive]:
        to_dict_cleaned = {k: v for k, v in asdict(self).items() if v not in (None, {}, [], "", 0, 0.0)}
        return to_dict_cleaned
