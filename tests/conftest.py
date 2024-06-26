import logging

import pytest

# noinspection PyUnresolvedReferences
from contextual.logging import ContextualLogger


@pytest.fixture(autouse=True)
def cleanup_test_logger_after_each_test():
    """
    Fixture to clean up the "test" logger after each test.

    As I keep creating a new logger named "test" in each test,
    I need to clean it up after each test to avoid memory leaks
    or undesired side effects.
    """
    yield

    logger_name = "test"
    if logger_name in logging.Logger.manager.loggerDict:
        logger = logging.getLogger(logger_name)
        for handler in logger.handlers[:]:
            logger.removeHandler(handler)
            handler.close()
        del logging.Logger.manager.loggerDict[logger_name]


@pytest.fixture(autouse=True)
def cleanup_contextual_logger_globals_after_each_test():
    """
    Fixture to clean up the global context and processors in the ContextualLogger after each test.

    As I keep modifying the global (static) context and processors in the ContextualLogger in each
    test, I need to clean them up after each test to avoid memory leaks or undesired side effects.
    """
    yield

    ContextualLogger._global_context = {}
    ContextualLogger._global_processors = {}
