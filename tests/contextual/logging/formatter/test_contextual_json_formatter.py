import json
import logging
from typing import Any, Dict

import pytest

from contextual.logging.formater import JsonFormatter
from contextual.logging.formater.attributes import (
    COMMON_LOG_RECORD_ATTRIBUTES,
    DEFAULT_LOG_RECORD_ATTRIBUTES_TO_EXCLUDE,
    OPTIONAL_LOG_RECORD_ATTRIBUTES,
    REQUEST_ID_ATTRIBUTE,
    TRACEABILITY_ID_ATTRIBUTE,
)


def test_formatter_should_output_a_valid_json_string():
    # Given
    under_test = JsonFormatter()
    # and
    record = a_valid_log_record()

    # When
    formatted = under_test.format(record)

    # Then
    assert isinstance(formatted, str)
    # and
    try:
        json_object = json.loads(formatted)
    except json.JSONDecodeError:
        pytest.fail("The output should be a valid JSON string")
    else:
        assert isinstance(json_object, dict), "The JSON object should be a dictionary"


def test_formatter_should_exclude_private_log_record_attributes():
    # Given
    under_test = JsonFormatter()
    record = a_valid_log_record({"_private_attribute": "test_private_value"})

    # When
    formatted = under_test.format(record)

    # Then
    json_object = json.loads(formatted)
    assert "_private_attribute" not in json_object, "Private attribute should not be in the formatted log record"


@pytest.mark.parametrize("attribute", list(DEFAULT_LOG_RECORD_ATTRIBUTES_TO_EXCLUDE))
def test_formatter_should_exclude_all_default_log_record_attributes(attribute):
    # Given
    under_test = JsonFormatter()
    record = a_valid_log_record()

    # When
    formatted = under_test.format(record)

    # Then
    json_object = json.loads(formatted)
    assert attribute not in json_object, f"Attribute '{attribute}' should not be in the formatted log record"


def test_formatter_should_error_when_common_application_name_attribute_is_missing():
    # Given
    under_test = JsonFormatter()
    record = a_valid_log_record()
    # and
    delattr(record, "application_name")

    # When
    with pytest.raises(ValueError) as e:
        under_test.format(record)

    # Then
    assert "_CommonLogProcessor: 'application_name' attribute is required" in str(e.value)


def test_formatter_should_generate_timestamp_even_if_created_attribute_is_missing():
    # Given
    under_test = JsonFormatter()
    record = a_valid_log_record()
    # and
    delattr(record, "created")

    # When
    formatted = under_test.format(record)

    # Then
    json_object = json.loads(formatted)
    assert "timestamp" in json_object, "Attribute 'timestamp' should be in the formatted log record"


@pytest.mark.parametrize(
    "attribute",
    list(OPTIONAL_LOG_RECORD_ATTRIBUTES | {REQUEST_ID_ATTRIBUTE, TRACEABILITY_ID_ATTRIBUTE}),
)
def test_formatter_should_support_optional_log_record_attributes(attribute):
    # Given
    under_test = JsonFormatter()
    record = a_valid_log_record({attribute: f"test_{attribute}_value"})

    # When
    formatted = under_test.format(record)

    # Then
    json_object = json.loads(formatted)
    assert attribute in json_object, f"Attribute '{attribute}' should be in the formatted log record"
    assert json_object[attribute] == f"test_{attribute}_value", f"Attribute '{attribute}' should have expected value"


def a_valid_log_record(kwargs: Dict[str, Any] = None):
    record = logging.LogRecord(
        name="test", level=logging.INFO, pathname=__file__, lineno=10, msg="Test message", args=(), exc_info=None
    )

    for a in COMMON_LOG_RECORD_ATTRIBUTES:
        setattr(record, a, f"test_{a.capitalize()}_value")

    # Add supplied attributes (if any)
    for a in kwargs or {}:
        setattr(record, a, kwargs[a])

    return record
