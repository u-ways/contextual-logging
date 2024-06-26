import traceback

from contextual.logging.model.error_log_record import ErrorLogRecord

# noinspection PyProtectedMember
from contextual.logging.processor.error_log_processor import _ErrorLogProcessor


def test_error_log_processor_process_without_exc_info():
    kwargs = {}
    processor = _ErrorLogProcessor()
    error_log_record = processor.process(kwargs)

    assert error_log_record is None


def test_error_log_processor_process_with_none_exc_info():
    kwargs = {"exc_info": None}
    processor = _ErrorLogProcessor()
    error_log_record = processor.process(kwargs)

    assert error_log_record is None


def test_error_log_processor_process_with_exc_info():
    # given
    kwargs = {"exc_info": (ValueError, ValueError("An error occurred"), None)}
    exc_class, exc_object, exc_traceback = kwargs["exc_info"]
    processor = _ErrorLogProcessor()

    # when
    error_log_record = processor.process(kwargs)

    # then
    assert error_log_record is not None
    assert isinstance(error_log_record, ErrorLogRecord)
    assert error_log_record.exception_type == "ValueError"
    assert error_log_record.exception_message == "An error occurred"
    assert error_log_record.exception_stack_trace == "".join(
        traceback.format_exception(exc_class, exc_object, exc_traceback)
    )
