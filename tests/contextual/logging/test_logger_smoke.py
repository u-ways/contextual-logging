"""
This test suite serves as a sanity check to ensure our logging
implementation didn't accidentally lose / override any of the standard
functionality we expect the Python logging utility to provide for us.
"""

import io
import logging
import logging.config
import sys
import tempfile
from pathlib import Path

from helpers import setup_stream_captor, write_to_file
from contextual.logging import ContextualLogger


def test_smoke_contextual_logger_should_still_be_able_to_stream_output_via_stdout():
    # Given
    under_test = ContextualLogger.create("test")
    under_test.setLevel(logging.INFO)
    # and
    log_stream, stream_handler = setup_stream_captor(under_test)

    # When
    under_test.info("test")
    # and
    stream_handler.flush()

    # Then
    assert "test" in log_stream.getvalue(), "Logger should output log message to stdout"


def test_smoke_contextual_logger_should_still_be_able_to_support_configration_via_configparser_file():
    log_captor = io.StringIO()
    original_stdout = sys.stdout
    sys.stdout = log_captor

    with tempfile.TemporaryDirectory() as temp_dir:
        configparser_configuration_path = write_to_file(
            file_path=Path(temp_dir, "logging_config.ini"),
            file_content="""
                [loggers]
                keys=root,test

                [handlers]
                keys=console

                [formatters]
                keys=simple

                [logger_root]
                level=DEBUG
                handlers=console

                [logger_test]
                level=DEBUG
                handlers=console
                qualname=test
                propagate=0

                [handler_console]
                class=StreamHandler
                level=DEBUG
                formatter=simple
                args=(sys.stdout,)

                [formatter_simple]
                format=%(asctime)s - %(name)s - %(levelname)s - %(message)s
                datefmt=%Y-%m-%d %H:%M:%S
                """,
        )

        try:
            # Given
            logging.config.fileConfig(configparser_configuration_path)
            under_test = ContextualLogger.create("test")

            # When
            under_test.debug("test")
            # And
            for handler in under_test.logger.handlers:
                if hasattr(handler, "flush"):
                    handler.flush()
        finally:
            sys.stdout = original_stdout

        # Then
        assert "test" in log_captor.getvalue(), "Logger should output log message to stdout"
