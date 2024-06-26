from abc import ABC, abstractmethod
from typing import TypeVar, Dict, Any, Generic

from contextual.logging.model import BaseLogRecord

LOG_RECORD = TypeVar("LOG_RECORD", bound=BaseLogRecord)


class BaseLogProcessor(ABC, Generic[LOG_RECORD]):
    """
    BaseLogProcessor is an abstract class that defines the interface for a log processor.

    You can create a custom log processor by extending this class and implementing the process method.
    One common use case is breaking down the extra attribute objects from the log record and adding
    them to the log message. (e.g. a request object becomes a request_method, request_url, request_headers,
    ...etc.)
    """

    @abstractmethod
    def process(self, kwargs: Dict[str, Any]) -> LOG_RECORD:
        """
        Allows you to extract (or create) custom log attributes from the log record attributes.
        The created log record attributes will eventually be added to the log message.

        :param kwargs: The log record attributes for a given log message
        :return: The custom log record attributes to enrich the log message
        """
        pass

    def extract_attribute(
        self,
        kwargs: Dict[str, Any],
        attribute_key: str,
        default_value: Any = None,
    ) -> Any:
        """
        Extract an attribute from the kwargs dictionary, if the attribute is not found, no default value is
        provided, or the default value is None, an exception is raised with a descriptive message.

        :param kwargs: The dictionary containing the attributes
        :param attribute_key: The key of the attribute to extract
        :param default_value: The default value to use if the attribute is not found
        :return: The attribute value if found
        """
        attribute_value = kwargs.get(attribute_key, default_value)

        if attribute_value is None:
            raise ValueError(f"{self.__class__.__name__}: '{attribute_key}' attribute is required")

        return attribute_value
