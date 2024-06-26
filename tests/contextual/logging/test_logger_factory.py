from contextual.logging import ContextualLogger


def test_factory_should_return_contextual_logger_instance():
    # When
    logger = ContextualLogger.create("test")

    # Then
    assert isinstance(logger, ContextualLogger), "Should return a contextual logger instance"


def test_factory_should_allow_setting_name_for_the_contextual_logger_instance():
    # Given
    name = "test"

    # When
    logger = ContextualLogger.create(name)

    # Then
    assert logger.name == name, "Should allow setting the name for the logger instance"


def test_factory_should_allow_setting_local_context_for_created_logger_instance_at_the_method_level():
    # Given
    local_context = {"request_url": "/test"}

    # When
    logger = ContextualLogger.create("test", local_context=local_context)

    # Then
    assert logger.local_context == local_context, "Should allow setting local context for the logger instance"
