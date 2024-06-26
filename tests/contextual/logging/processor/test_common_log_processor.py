import time
from datetime import datetime, timezone

import pytest

from contextual.logging.model.common_log_record import CommonLogRecord

# noinspection PyProtectedMember
from contextual.logging.processor.common_log_processor import _CommonLogProcessor


def test_common_log_processor_with_all_attributes():
    # given
    kwargs = {
        "application_name": "test_application_name",
        "levelname": "INFO",
        "created": time.time(),
    }

    # when
    result = _CommonLogProcessor().process(kwargs)

    # then
    assert_log_record(result, "test_application_name", "INFO", kwargs["created"])


def test_common_log_processor_raises_error_for_missing_application_name():
    # given
    kwargs = {
        "levelname": "INFO",
        "created": time.time(),
    }

    # when
    with pytest.raises(ValueError) as excinfo:
        _CommonLogProcessor().process(kwargs)

    # then
    assert str(excinfo.value) == "_CommonLogProcessor: 'application_name' attribute is required"


def test_common_log_processor_raises_error_for_missing_log_level():
    # given
    kwargs = {
        "application_name": "test_application_name",
        "created": time.time(),
    }

    # when
    with pytest.raises(ValueError) as excinfo:
        _CommonLogProcessor().process(kwargs)

    # then
    assert str(excinfo.value) == "_CommonLogProcessor: 'levelname' attribute is required"


def test_common_log_processor_uses_current_time_if_created_not_provided():
    # given
    kwargs = {
        "application_name": "test_application_name",
        "levelname": "INFO",
    }

    # when
    result = _CommonLogProcessor().process(kwargs)

    # then
    assert_log_record(result, "test_application_name", "INFO", None)


def test_common_log_processor_with_invalid_created_time():
    # given
    kwargs = {
        "application_name": "test_application_name",
        "levelname": "INFO",
        "created": "invalid_time",
    }

    # when / then
    with pytest.raises(ValueError):
        _CommonLogProcessor().process(kwargs)


def assert_log_record(log_record, application_name, levelname, created):
    assert isinstance(log_record, CommonLogRecord)
    assert log_record.application_name == application_name
    assert log_record.log_level == levelname
    if created is not None:
        assert log_record.timestamp == datetime.fromtimestamp(created, tz=timezone.utc).isoformat(
            timespec="microseconds"
        )
    else:
        assert datetime.fromisoformat(log_record.timestamp).tzinfo == timezone.utc
