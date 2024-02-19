import converter
import pytest
from exceptions import InvalidDictError


class TestConverter:

    def test_when_dikt_is_single_level_with_native_values(self):
        converted = converter.convert(dikt="{'name': 'mridula'}")
        assert converted == '{"name":"mridula"}'

    def test_when_dikt_with_beautify(self):
        converted = converter.convert(dikt="{'name': 'mridula'}", beautify=True)
        assert converted == '{\n  "name": "mridula"\n}'

    def test_when_dikt_with_two_levels(self):
        converted = converter.convert(
            dikt="{'name': 'mridula', 'address': {'city': 'Mumbai'}}"
        )
        assert converted == '{"name":"mridula","address":{"city":"Mumbai"}}'

    def test_when_dikt_is_not_valid(self):
        with pytest.raises(InvalidDictError) as e:
            converter.convert(dikt="Lorem ipsum")

    def test_when_dikt_has_datetime(self):
        converted = converter.convert(dikt="{'name': datetime.datetime.now()}")
        assert converted == '{"name":"datetime.datetime.now()"}'

    def test_when_dikt_has_object(self):
        converted = converter.convert(
            dikt="{'name': <object object at 0x7f83fa0631b0>}"
        )
        assert converted == '{"name":"<object object at 0x7f83fa0631b0>"}'

    def test_when_dikt_has_an_unrecognized_function_call(self):
        converted = converter.convert(dikt="{'name': SyntaxError()}")
        assert converted == '{"name":"SyntaxError()"}'
