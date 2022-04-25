import pytest
from . import ArgumentsHelper

class Test_remove_flags:
    def test_remove_when_has_resources_and_flag(self):
        arguments = 'My Resource --flag value'
        result = ArgumentsHelper().remove_flags(arguments)
        assert result == 'My Resource'

    def test_remove_when_has_no_flags(self):
        arguments = 'My Resource'
        result = ArgumentsHelper().remove_flags(arguments)
        assert result == 'My Resource'

    def test_remove_when_has_no_resource(self):
        arguments = '--flag value'
        result = ArgumentsHelper().remove_flags(arguments)
        assert result == ''

class Test_extract_flags:
    def test_extract_when_has_multiple_flags(self):
        arguments = 'My Resource --flag1 value --flag2 another value with spaces'
        result = ArgumentsHelper().extract_flags(arguments)
        assert result['flag1'] == 'value'
        assert result['flag2'] == 'another value with spaces'

    def test_extract_when_has_no_flags(self):
        arguments = 'My Resource'
        result = ArgumentsHelper().extract_flags(arguments)
        assert len(result.keys()) == 0

    def test_extract_when_has_no_resource(self):
        arguments = '--flag value'
        result = ArgumentsHelper().extract_flags(arguments)
        assert result['flag'] == 'value'

    def test_extract_with_validator(self):
        arguments = 'My Resource --flag value'
        validators = {
            'flag': lambda _: True
        }
        result = ArgumentsHelper().extract_flags(arguments, validators)
        assert result['flag'] == 'value'

    def test_dont_extract_when_validation_fails(self):
        arguments = 'My resource --flag value'
        validators = {
            'flag' : lambda _: ().throw(Exception('Exception'))
        }
        with pytest.raises(Exception):
            ArgumentsHelper().extract_flags(arguments, validators)

class Test_check_required_flags:
    required_flags = 'flag-a flag-b'

    def test_check_successfully(self):
        extracted_flags = {
            'flag-a': 'value-a',
            'flag-b': 'value-b',
            'flag-c': 'value-c',
        }
        try:
            ArgumentsHelper().check_required_flags(self.required_flags.split(' '), self.required_flags, extracted_flags)
        except Exception as exc:
            assert False, f"'check_required_flags' raised an exception {exc}"

    def test_check_fails_when_missing_required_flags(self):
        extracted_flags = {
            'flag-c': 'value-c'
        }
        with pytest.raises(Exception):
            ArgumentsHelper().check_required_flags(self.required_flags.split(' '), self.required_flags, extracted_flags)

    def test_check_successfully_when_required_flags_are_not_valid(self):
        extracted_flags = {
            'flag-a': 'value-a',
        }
        try:
            ArgumentsHelper().check_required_flags(['flag-d', 'flag-e'], self.required_flags, extracted_flags)
        except Exception as exc:
            assert False, f"'check_required_flags' raised an exception {exc}"
