from contextual.logging.model.common_log_record import CommonLogRecord


def test_common_log_record_to_dict_should_place_fields_in_top_level():
    # Given
    record = CommonLogRecord(
        application_name="Entity",
        timestamp="2021-01-01T00:00:00.000000+00:00",
        log_level="INFO",
    )
    # When
    result = record.to_dict()

    # Then
    assert result == {
        "application_name": "Entity",
        "timestamp": "2021-01-01T00:00:00.000000+00:00",
        "log_level": "INFO",
    }
