import logging
from dataclasses import dataclass
from typing import Dict, Any

from helpers import setup_stream_captor

from contextual.logging import ContextualLogger
from contextual.logging.model import BaseLogRecord
from contextual.logging.processor import BaseLogProcessor


def test_process_should_preserve_extra_record_attributes():
    # Given
    under_test = ContextualLogger.create("test")
    under_test.setLevel(logging.INFO)
    # and
    log_stream, stream_handler = setup_stream_captor(under_test)
    # and
    stream_handler.setFormatter(logging.Formatter("%(message)s %(extra)s"))

    # When
    under_test.info("test", extra={"extra": "extra_application_name"})
    # and
    stream_handler.flush()

    # Then
    assert log_stream.getvalue().strip() == "test extra_application_name"


def test_process_should_set_global_context_as_record_attributes():
    # Given
    under_test = ContextualLogger.create("test")
    under_test.setLevel(logging.INFO)
    # and
    log_stream, stream_handler = setup_stream_captor(under_test)
    # and
    stream_handler.setFormatter(logging.Formatter("%(message)s %(application_name)s"))

    # When
    ContextualLogger.set_global_context(application_name="global_context_value")
    # and
    under_test.info("test")
    # and
    stream_handler.flush()

    # Then
    assert log_stream.getvalue().strip() == "test global_context_value"


def test_process_should_set_local_context_as_record_attributes():
    # Given
    under_test = ContextualLogger.create("test")
    under_test.setLevel(logging.INFO)
    # and
    log_stream, stream_handler = setup_stream_captor(under_test)
    # and
    stream_handler.setFormatter(logging.Formatter("%(message)s %(local_context_key)s"))

    # When
    under_test.local_context = {"local_context_key": "local_context_value"}
    # and
    under_test.info("test")
    # and
    stream_handler.flush()

    # Then
    assert log_stream.getvalue().strip() == "test local_context_value"


def test_process_should_be_able_to_handle_both_local_and_global_context_as_record_attributes():
    # Given
    under_test = ContextualLogger.create("test")
    under_test.setLevel(logging.INFO)
    # and
    log_stream, stream_handler = setup_stream_captor(under_test)
    # and
    stream_handler.setFormatter(logging.Formatter("%(message)s %(global_context_key)s %(local_context_key)s"))

    # When
    ContextualLogger.set_global_context(
        application_name="some_application_name", kwargs={"global_context_key": "global_context_value"}
    )
    # and
    under_test.local_context = {"local_context_key": "local_context_value"}
    # and
    under_test.info("test")
    # and
    stream_handler.flush()

    # Then
    assert log_stream.getvalue().strip() == "test global_context_value local_context_value"


def test_process_should_correctly_apply_a_global_processors_to_log_record():
    # Given
    under_test = ContextualLogger.create("test")
    under_test.setLevel(logging.INFO)
    # and
    log_stream, stream_handler = setup_stream_captor(under_test)
    # and
    stream_handler.setFormatter(logging.Formatter("%(log_attribute)s"))

    # When
    ContextualLogger.set_global_processors(TestLogProcessor())
    # and
    under_test.info("test", extra={"_log_attribute": "some_value"})
    # and
    stream_handler.flush()

    # Then
    assert log_stream.getvalue().strip() == "some_value"


def test_process_should_allow_stacking_multiple_global_processors():
    # Given
    under_test = ContextualLogger.create("test")
    under_test.setLevel(logging.INFO)
    # and
    log_stream, stream_handler = setup_stream_captor(under_test)
    # and
    stream_handler.setFormatter(logging.Formatter("%(log_attribute)s %(log_attribute_2)s"))

    # When
    ContextualLogger.set_global_processors(TestLogProcessor(), TestLogProcessor2())
    # and
    under_test.info("test", extra={"_log_attribute": "some_value", "_log_attribute_2": "some_value_2"})
    # and
    stream_handler.flush()

    # Then
    assert log_stream.getvalue().strip() == "some_value some_value_2"


@dataclass
class TestLogRecord(BaseLogRecord):
    log_attribute: str = ""


class TestLogProcessor(BaseLogProcessor[TestLogRecord]):
    def process(self, kwargs: Dict[str, Any]) -> TestLogRecord:
        log_attribute = self.extract_attribute(kwargs, "_log_attribute")
        return TestLogRecord(log_attribute)


@dataclass
class TestLogRecord2(BaseLogRecord):
    log_attribute_2: str = ""


class TestLogProcessor2(BaseLogProcessor[TestLogRecord2]):
    def process(self, kwargs: Dict[str, Any]) -> TestLogRecord2:
        log_attribute_2 = self.extract_attribute(kwargs, "_log_attribute_2")
        return TestLogRecord2(log_attribute_2)
