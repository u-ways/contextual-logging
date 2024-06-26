import io
import logging
import logging.config
from pathlib import Path

# noinspection PyUnresolvedReferences
from contextual.logging import ContextualLogger


def setup_stream_captor(under_test: ContextualLogger) -> tuple[io.StringIO, logging.StreamHandler]:
    """
    Setups a string stream captor for the given logger
    This is useful for testing log messages output in unit tests.

    :param under_test: The contextual logger to setup the stream captor for.
    """
    log_stream = io.StringIO()
    stream_handler = logging.StreamHandler(log_stream)
    under_test.logger.addHandler(stream_handler)
    return log_stream, stream_handler


def write_to_file(file_path: Path, file_content: str) -> Path:
    """
    Writes the given content to the given file path and returns the file path.

    :param file_path: The file path to write to
    :param file_content: The content to write to the file
    """
    file_path.write_text(file_content)
    return file_path
