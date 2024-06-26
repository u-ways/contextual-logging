from dataclasses import dataclass, fields
from typing import Any, Type, TypeVar


@dataclass(frozen=True)
class _GetFields:
    """
    _GetFields is a class that provides a way to access the field names of a dataclass model.

    This is useful for building a type-safe system that will break when the model's field names change
    without updating the dependent code.
    """

    _model: Type[Any]

    def __getattr__(self, item: str) -> str:
        # noinspection PyDataclass
        for field in fields(self._model):
            if field.name == item:
                return item
        raise AttributeError(f"'{self._model.__name__}' object has no attribute '{item}'")


DATA_CLASS = TypeVar("DATA_CLASS", bound=Type[Any])


def get_fields(model: DATA_CLASS) -> _GetFields:
    """
    get_fields is a function that returns an instance of _GetFields.

    :param model: The dataclass model to get the fields from
    :return: An instance of _GetFields
    """
    return _GetFields(model)
