from dataclasses import dataclass

import pytest

# noinspection PyProtectedMember
from contextual.logging.hinting.fields_collector import get_fields, _GetFields


@dataclass
class SampleDataClass:
    field1: int
    field2: str
    field3: float


def test_get_fields_should_return_correct_instance():
    fields_obj = get_fields(SampleDataClass)
    assert isinstance(fields_obj, _GetFields)


def test_get_field_should_return_correct_field_name():
    fields_obj = get_fields(SampleDataClass)
    assert fields_obj.field1 == "field1"
    assert fields_obj.field2 == "field2"
    assert fields_obj.field3 == "field3"


def test_get_field_should_raise_attribute_error_when_field_does_not_exist():
    fields_obj = get_fields(SampleDataClass)

    with pytest.raises(AttributeError) as e:
        _ = fields_obj.field4

    assert "'SampleDataClass' object has no attribute 'field4'" in str(e.value)
