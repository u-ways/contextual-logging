import pytest
from typing import Dict, Any
from contextual.logging.model import BaseLogRecord
from contextual.logging.processor import BaseLogProcessor


def test_base_log_processor_process_method_should_return_the_log_record_instance_it_types():
    log_record = TestLogProcessor().process({"log_message": "value"})
    assert isinstance(log_record, TestLogRecord)


def test_base_log_processor_extract_attribute_method_should_return_the_attribute_value_when_present():
    kwargs = {"log_message": "This is a log message"}
    attribute_value = TestLogProcessor().extract_attribute(kwargs, "log_message")
    assert attribute_value == "This is a log message"


def test_base_log_processor_extract_attribute_method_should_use_default_value_if_given_when_attribute_not_present():
    default_value = "Default message"
    attribute_value = TestLogProcessor().extract_attribute({}, "log_message", default_value)
    assert attribute_value == default_value


def test_base_log_processor_extract_attribute_method_should_raise_value_error_when_attribute_is_not_present():
    with pytest.raises(ValueError) as excinfo:
        TestLogProcessor().extract_attribute({}, "log_message")
    assert str(excinfo.value) == "TestLogProcessor: 'log_message' attribute is required"


class TestLogRecord(BaseLogRecord):
    def __init__(self, log_message: str):
        self.log_message = log_message


class TestLogProcessor(BaseLogProcessor[TestLogRecord]):
    def process(self, kwargs: Dict[str, Any]) -> TestLogRecord:
        log_message = self.extract_attribute(kwargs, "log_message")
        return TestLogRecord(log_message)
