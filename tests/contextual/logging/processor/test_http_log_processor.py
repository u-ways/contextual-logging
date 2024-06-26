"""
NOTE:
    We should load some web framework request and response objects and
    create our own custom base log processor to adapt the request and response
    objects to the standard log attributes. (import them via test scope ONLY)

GREAT IDEA:
    Because we filter an private fields (i.e. prefixed with '_') in the log record,
    we can create "transit" objects that will be used to adapt the request and response.

    e.g. logger.info("Request", extra={"_request": request, "_response": response})

    Then we can create a custom base log processor that will adapt the request and response.
"""

# IDEA: Can we merge the similar tests into a single test case?

# FastAPI Web Framework


def test_process_should_adapt_starlette_request_object_to_standard_http_attributes():
    pass


def test_process_should_adapt_starlette_response_object_to_standard_http_attributes():
    pass


def test_process_should_adapt_starlette_x_request_id_header_to_standard_request_id_log_attribute():
    pass


def test_process_should_adapt_starlette_x_correlation_id_header_to_standard_correlation_id_log_attribute():
    pass


# Flask Web Framework


def test_process_should_adapt_flask_request_object_to_standard_http_attributes():
    pass


def test_process_should_adapt_flask_response_object_to_standard_http_attributes():
    pass


def test_process_should_adapt_flask_x_request_id_header_to_standard_request_id_log_attribute():
    pass


def test_process_should_adapt_flask_x_correlation_id_header_to_standard_correlation_id_log_attribute():
    pass
