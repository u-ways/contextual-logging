import io
import re
import sys
import tempfile
from pathlib import Path

import pytest

from helpers import write_to_file
from contextual.logging import ContextualLogger


def test_yaml_loader_should_fail_when_file_not_found():
    # Given
    yaml_configuration_path = Path("non_existent_file.yaml")

    # When
    with pytest.raises(FileNotFoundError) as exc_info:
        ContextualLogger.configuration_from(yaml_configuration_path)

    # Then
    assert str(exc_info.value) == f"Supplied configuration file is not found at: {yaml_configuration_path}"


def test_yaml_loader_should_fail_when_yaml_content_is_invalid():
    with tempfile.TemporaryDirectory() as temp_dir:
        # Given
        yaml_configuration_path = write_to_file(
            file_path=Path(temp_dir, ContextualLogger.CONFIGURATION_FILENAME),
            file_content="""Some invalid yaml content""",
        )

        # When
        with pytest.raises(ValueError) as exc_info:
            ContextualLogger.configuration_from(yaml_configuration_path)

        # Then
        assert re.search(
            r"Error parsing the supplied configuration file: .*", str(exc_info.value)
        ), "Exception message should match the expected pattern"


def test_yaml_loader_should_correctly_load_a_valid_yaml_file():
    log_captor = io.StringIO()
    original_stdout = sys.stdout
    sys.stdout = log_captor

    with tempfile.TemporaryDirectory() as temp_dir:
        yaml_configuration_path = write_to_file(
            file_path=Path(temp_dir, ContextualLogger.CONFIGURATION_FILENAME),
            file_content="""
                version: 1
                disable_existing_loggers: False

                formatters:
                  simple:
                    format: '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
                    datefmt: '%Y-%m-%d %H:%M:%S'
                  json:
                    format: '%(message)s'
                    class: contextual.logging.formater.JsonFormatter

                handlers:
                  console-json:
                    class: logging.StreamHandler
                    formatter: json
                    stream: ext://sys.stdout
                  console-simple:
                    class: logging.StreamHandler
                    formatter: simple
                    stream: ext://sys.stdout

                loggers:
                  test:
                    level: DEBUG
                    handlers:
                      - console-json
                    propagate: no

                root:
                  level: ERROR
                  handlers:
                    - console-simple
                """,
        )

        try:
            # Given
            ContextualLogger.configuration_from(yaml_configuration_path)
            ContextualLogger.set_global_context(application_name="test")
            under_test = ContextualLogger.create("test")

            # When
            under_test.debug("test", extra={"some_test": "test"})
            # And
            for handler in under_test.logger.handlers:
                if hasattr(handler, "flush"):
                    handler.flush()
        finally:
            sys.stdout = original_stdout

        # Then
        assert "test" in log_captor.getvalue(), "Logger should output log message to stdout"
