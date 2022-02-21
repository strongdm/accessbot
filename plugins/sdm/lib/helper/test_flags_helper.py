import pytest
from . import FlagsHelper


class Test_remove_flags:
    def test_remove_when_has_resources_and_flag(self):
        arguments = 'My Resource --flag value'
        result = FlagsHelper().remove_flags(arguments)
        assert result == 'My Resource'

    def test_remove_when_has_no_flags(self):
        arguments = 'My Resource'
        result = FlagsHelper().remove_flags(arguments)
        assert result == 'My Resource'
        
    def test_remove_when_has_no_resource(self):
        arguments = '--flag value'
        result = FlagsHelper().remove_flags(arguments)
        assert result == ''


class Test_extract_flags:
    def test_extract_when_has_multiple_flags(self):
        arguments = 'My Resource --flag1 value --flag2 another value with spaces'
        result = FlagsHelper().extract_flags(arguments)
        assert result['flag1'] == 'value'
        assert result['flag2'] == 'another value with spaces'

    def test_extract_when_has_no_flags(self):
        arguments = 'My Resource'
        result = FlagsHelper().extract_flags(arguments)
        assert len(result.keys()) == 0

    def test_extract_when_has_no_resource(self):
        arguments = '--flag value'
        result = FlagsHelper().extract_flags(arguments)
        assert result['flag'] == 'value'

    def test_extract_with_validator(self):
        arguments = 'My Resource --flag value'
        validators = {
            'flag': lambda _: True
        }
        result = FlagsHelper().extract_flags(arguments, validators)
        assert result['flag'] == 'value'

    def test_dont_extract_when_validation_fails(self):
        arguments = 'My resource --flag value'
        validators = {
            'flag' : lambda _: ().throw(Exception('Exception'))
        }
        with pytest.raises(Exception):
            FlagsHelper().extract_flags(arguments, validators)
