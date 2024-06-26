import logging
from collections.abc import MutableMapping
from logging import config
from pathlib import Path
from typing import Any, Dict, Tuple, override, Mapping

import yaml

from contextual.logging.hinting import Primitive, EXTRA_ARGUMENT
from contextual.logging.hinting.fields_collector import get_fields
from contextual.logging.model.common_log_record import CommonLogRecord
from contextual.logging.processor import BaseLogProcessor


class ContextualLogger(logging.LoggerAdapter):
    """
    A contextual logger implementation that allows the user to effectively add context to log messages.

    This logger is a wrapper around the standard Python logger that allows the user to add context to log messages.
    The context can be added at two levels:

    1. Global Context: used for attributes that are added to all logger instances. This is useful for adding common
       details to all log messages regardless of logger instance. (e.g. application name, environment, etc.)

    2. Local Context: used for attributes that are added to whichever (single) logger instance you have instantiated.
       This is useful for adding details that are specific to a particular logger for the application. (e.g.
       you've created a logger for a particular file, and you want to add the file name to all log messages for
       that logger instance.)

       It's important to note that the local context is mutable and can be set, updated, and cleared at any time. Unlike
       the extra argument in the standard Python logger, the local context is not a one-time addition to the log message
       but a mutable local context that can impact all users of the same logger instance until it is cleared.

    For one time addition of context to a log message, you can use the extra argument in the standard Python logger.

    e.g.

    ```python
    logger.info("This is a log message", extra={"correlation_id": "1234"})
    ```
    """

    CONFIGURATION_FILENAME = "logging_config.yaml"

    _global_context: Mapping[str, Primitive] = {}
    _global_processors: set[BaseLogProcessor] = {}

    def __init__(self, name: str = __name__, local_context: MutableMapping[str, Primitive] = None):
        self._local_context = local_context if local_context is not None else {}
        super().__init__(logging.getLogger(name))

    @classmethod
    def create(cls, name: str, local_context: MutableMapping[str, Primitive] = None) -> "ContextualLogger":
        """
        A factory method to create a contextual logger instance.

        Please use this method to create a logger instance instead of directly instantiating the class. This helps
        in keeping the code consistent and future-proof as we can change the logger implementation without affecting
        the client code.

        :param name:           The name of the logger
        :param local_context:  Clearable context that can be added to log messages, this is useful for adding details
                               that are specific to a particular lifecycle of the application. (e.g. correlation id,
                               user id, request url, etc.)
        :return:               A contextual logger instance
        """

        return cls(name, local_context)

    @staticmethod
    def set_global_context(application_name: str, kwargs: Mapping[str, Primitive] = None) -> None:
        """
        Set the global context The global context to be added to all log messages, this is useful for adding common
        details to all log messages. (e.g. application name (application_name), module name (module), etc...)

        This is usually set once at the start of the application.

        e.g.

        ```python
        ContextualLogger.set_global_context(
            application_name="my_app",
            {"additional_key": "additional_value"}
        )
        ```
        """
        if kwargs is None:
            kwargs = {}

        if application_name is not None:
            kwargs[get_fields(CommonLogRecord).application_name] = application_name

        ContextualLogger._global_context = kwargs

    @staticmethod
    def set_global_processors(*processors: BaseLogProcessor) -> None:
        """
        Set the global processors to be used to enrich the log message with custom attributes.

        This is usually set once at the start of the application.

        e.g.

        ```python
        ContextualLogger.set_global_processors({MyCustomHttpLogProcessor()})
        ```
        """
        ContextualLogger._global_processors = set(processors)

    @staticmethod
    def configuration_from(path: Path) -> None:
        """
        Set the global logging configuration from a YAML file.

        This is usually set once at the start of the application.

        e.g.

        ```python
        ContextualLogger.configuration_from(Path("path/to/" + ContextualLogger.CONFIGURATION_FILENAME))
        ```

        :param path: The path to the YAML configuration file

        For more information on what you can add to the YAML configuration file,
        see: https://docs.python.org/3/library/logging.config.html
        """
        try:
            with path.open() as file:
                config_from_yaml = yaml.safe_load(file)
            config.dictConfig(config_from_yaml)
        except FileNotFoundError:
            raise FileNotFoundError(f"Supplied configuration file is not found at: {path}")
        except Exception as e:
            raise ValueError(f"Error parsing the supplied configuration file: {e}")

    @override
    def process(self, msg: str, kwargs: Dict[str, Any]) -> Tuple[str, Dict[str, Any]]:
        """
        Within the logging adapter, the process method is called just before the log record is created.
        As such, this gives us the power to modify the log message and the log record attributes before it is created.

        In our case, we are using this method to enrich the log with the global and local context.

        :param msg:     The log message
        :param kwargs:  The log record attributes
        :return:        The modified log message and log record attributes
        """
        initial_context = {
            **ContextualLogger._global_context,
            **self._local_context,
            **(kwargs.get(EXTRA_ARGUMENT) or {}),
        }

        enriched_context = {}
        for p in ContextualLogger._global_processors:
            enriched_context = {**enriched_context, **p.process(initial_context).to_dict()}

        kwargs[EXTRA_ARGUMENT] = initial_context | enriched_context

        return msg, kwargs

    @property
    def local_context(self) -> MutableMapping[str, Primitive]:
        """
        Get the local context that is added to log messages.

        This is useful for adding more context details in a mutable way via the setter. e.g.

        ```python
        logger.local_context["file_name"] = "my_file.py"
        ```
        """
        if self._local_context is None:
            self._local_context = {}
        return self._local_context

    @local_context.setter
    def local_context(self, value: MutableMapping[str, Primitive]) -> None:
        """
        Override (or set) the local_context context property that is added to log messages.

        This is useful for setting the local context details in bulk. e.g.

        ```python
        logger.local_context = {"file_name": "my_file.py", "package_name": "my_package"}
        ```
        """
        self._local_context = value

    @local_context.deleter
    def local_context(self) -> None:
        """
        Clear the local_context context that is added to log messages.

        This is useful for removing the local context if they're no longer needed. e.g.

        ```python
        del logger.local_context
        ```
        """
        self._local_context = {}
