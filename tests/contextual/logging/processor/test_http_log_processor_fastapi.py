"""
NOTE:
    This test file is a source of documentation for creating your own HTTP log processor.

    We are loading some common web frameworks request and response objects and
    adapting them to our standard HTTP log record attributes with a custom http log
    processor extending the BaseLogProcessor as an example.

TIP:
    Because we filter an private fields (i.e. prefixed with '_') in the log record,
    we can create "transit" objects that will be used to adapt the request and response.

    e.g. logger.info("Request", extra={"_request": request, "_response": response})

    This allows us to decongest the log message and keep the log message clean and concise.
    (i.e. we break down those objects into their respective attributes in the log processor)
"""

from typing import Dict, Any

import starlette.requests
import starlette.responses

from contextual.logging.formater.attributes import REQUEST_ID_ATTRIBUTE
from contextual.logging.model.http_log_record import HttpLogRecord
from contextual.logging.processor import BaseLogProcessor


def test_process_should_adapt_starlette_request_object_to_standard_http_attributes():
    # given
    request = starlette.requests.Request(
        scope={
            "type": "http",
            "method": "GET",
            "path": "/some/path",
            "query_string": b"some=query&params=here",
            "headers": [(b"host", b"test.com")],
        }
    )
    # and
    kwargs = {
        "_request": request,
    }

    # when
    result = FastApiLogProcessor().process(kwargs)

    # Then
    assert result.request_method == "GET"
    # noinspection HttpUrlsUsage
    assert result.request_url == "http://test.com/some/path?some=query&params=here"
    assert result.request_query_params == {"some": "query", "params": "here"}
    assert result.request_headers == {"host": "test.com"}


def test_process_should_adapt_starlette_response_object_to_standard_http_attributes():
    # given
    response = starlette.responses.Response(
        status_code=200,
        headers={"content-type": "application/json", "content-length": "1234"},
    )
    # and
    kwargs = {
        "_response": response,
    }

    # when
    result = FastApiLogProcessor().process(kwargs)

    # Then
    assert result.response_status == 200
    assert result.response_headers == {"content-type": "application/json", "content-length": "1234"}


def test_process_should_adapt_starlette_x_request_id_header_to_standard_request_id_log_attribute():
    # given
    request = starlette.requests.Request(
        scope={
            "type": "http",
            "method": "GET",
            "path": "/",
            "query_string": b"",
            "headers": [(b"x-request-id", b"1234")],
        }
    )
    # and
    kwargs = {
        "_request": request,
    }

    # when
    result = FastApiLogProcessor().process(kwargs)

    # Then
    assert result.request_id == "1234"


def test_process_should_adapt_response_duration_ms_to_standard_response_duration_ms_log_attribute():
    # given
    kwargs = {
        "_response_duration_ms": 123.456,
    }

    # when
    result = FastApiLogProcessor().process(kwargs)

    # Then
    assert result.response_duration_ms == 123.456


class FastApiLogProcessor(BaseLogProcessor[HttpLogRecord]):
    def process(self, kwargs: Dict[str, Any]) -> HttpLogRecord:
        request: starlette.requests.Request = kwargs.get("_request")
        response: starlette.responses.Response = kwargs.get("_response")
        response_duration_ms: float = kwargs.get("_response_duration_ms")

        record = HttpLogRecord()

        if request is not None:
            record.request_method = request.method
            record.request_url = str(request.url)
            record.request_query_params = dict(request.query_params) if request.query_params else {}
            record.request_headers = dict(request.headers) if request.headers else {}

            request_id = request.headers.get("x-request-id", kwargs.get(REQUEST_ID_ATTRIBUTE))

            if request_id is not None:
                record.request_id = request_id

        if response is not None:
            record.response_status = response.status_code
            record.response_headers = dict(response.headers) if response.headers else {}

        if response_duration_ms is not None:
            record.response_duration_ms = response_duration_ms

        return record
