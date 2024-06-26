from typing import Union

"""
A primitive is a data type that is not an object and has no methods.

This is useful for type hinting when you want to guide the user to use primitive types only for a variable.
"""
Primitive = Union[int, float, str, bool]

"""
A static reference for the fourth keyword argument in the logging.Logger.log method.

The extra used to pass a dictionary which is used to populate the __dict__ of the LogRecord
created for the logging event with user-defined attributes. We heavily rely on this argument
to enrich the log message with extra attributes.

See: https://docs.python.org/3/library/logging.html#logging.Logger.debug
"""
EXTRA_ARGUMENT = "extra"
