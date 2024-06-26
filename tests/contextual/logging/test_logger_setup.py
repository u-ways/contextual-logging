import logging

from contextual.logging import ContextualLogger


def test_contextual_logger_should_return_logger_adapter_instance():
    # Given
    logger = ContextualLogger()

    # Then
    assert isinstance(logger, logging.LoggerAdapter), "ContextualLogger should be an instance of LoggerAdapter"


def test_contextual_logger_should_allow_setting_logger_name():
    # Given
    logger = ContextualLogger("test")

    # Then
    assert logger.logger.name == "test", "ContextualLogger should allow setting logger name"


def test_contextual_logger_should_allow_setting_global_context_value_at_a_static_scope():
    # Given
    application_name = "test"
    global_context = {"key": "value"}

    # When
    ContextualLogger.set_global_context(application_name=application_name, kwargs=global_context)
    logger = ContextualLogger()

    # Then
    assert logger._global_context == {
        **global_context,
        "application_name": application_name,
    }, "ContextualLogger should allow setting global context value at a static scope"


def test_contextual_logger_should_propagate_setting_the_global_context_across_all_instances():
    # Given
    global_context = {"application_name": "test"}

    # When
    ContextualLogger.set_global_context(application_name="test")
    logger_1 = ContextualLogger()
    logger_2 = ContextualLogger()

    # Then
    assert logger_1._global_context == global_context, "ContextualLogger should propagate setting the global context"
    assert logger_2._global_context == global_context, "ContextualLogger should propagate setting the global context"


def test_contextual_logger_should_allow_setting_local_context_value_at_a_constructor_scope():
    # Given
    logger = ContextualLogger(local_context={"key": "value"})

    # When
    value = logger.local_context["key"]

    # Then
    assert value == "value", "ContextualLogger should allow setting local context value at a constructor scope"


def test_contextual_logger_should_allow_setting_local_context_value_at_a_class_property_scope():
    # Given
    logger = ContextualLogger()

    # When
    logger.local_context["key"] = "value"
    value = logger.local_context["key"]

    # Then
    assert value == "value", "ContextualLogger should allow setting local context value at a class property scope"


def test_contextual_logger_should_allow_clearing_local_context_context_value():
    # Given
    logger = ContextualLogger()
    logger.local_context["key"] = "value"

    # When
    del logger.local_context["key"]

    # Then
    assert "key" not in logger.local_context, "ContextualLogger should allow clearing local_context context value"


def test_contextual_logger_should_not_propagate_setting_the_local_context_across_all_instances():
    # Given
    logger_1 = ContextualLogger()
    logger_2 = ContextualLogger()

    # When
    logger_1.local_context["key"] = "value"

    # Then
    assert "key" not in logger_2.local_context, "ContextualLogger should not propagate setting the local context"
