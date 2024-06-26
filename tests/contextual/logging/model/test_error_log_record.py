from contextual.logging.model.error_log_record import ErrorLogRecord


def test_error_log_record_should_wrap_error_fields_in_error_key():
    # Given
    record = ErrorLogRecord(
        exception_type="Exception",
        exception_message="An error occurred",
        exception_stack_trace="A given stack traceback",
    )
    # When
    result = record.to_dict()

    # Then
    assert result == {
        "error": {
            "exception_type": "Exception",
            "exception_message": "An error occurred",
            "exception_stack_trace": "A given stack traceback",
        }
    }
