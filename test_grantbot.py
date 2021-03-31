from errbot.backends.base import Message
import pytest
import sys
import time
from unittest.mock import MagicMock

sys.path.append('plugins/sdm')
from properties import Properties

pytest_plugins = ["errbot.backends.test"]
extra_plugin_dir = 'plugins/sdm'

def test_help_command(testbot):
    testbot.push_message("help")
    assert "access to resource-name" in testbot.pop_message()

def test_access_command_grant_approved(testbot):
    mock_dict = {
        'service': get_service_mock(), 
        'props': get_props_fake()
    }
    testbot.inject_mocks('GrantBot', mock_dict)
    testbot.push_message("access to Xxx")
    testbot.push_message("yes")
    assert "valid request" in testbot.pop_message()
    assert "access request" in testbot.pop_message()
    assert "Granting" in testbot.pop_message()

def test_access_command_grant_timed_out(testbot):
    mock_dict = {
        'service': get_service_mock(), 
        'props': get_props_fake()
    }
    testbot.inject_mocks('GrantBot', mock_dict)
    testbot.push_message("access to Xxx")
    assert "valid request" in testbot.pop_message()
    assert "access request" in testbot.pop_message()
    assert "timed out" in testbot.pop_message()
    assert "not approved" in testbot.pop_message()

def test_access_command_grant_not_approved(testbot):
    mock_dict = {
        'service': get_service_mock(), 
        'props': get_props_fake()
    }
    testbot.inject_mocks('GrantBot', mock_dict)
    testbot.push_message("access to Xxx")
    testbot.push_message("no") # Anything but yes
    assert "valid request" in testbot.pop_message()
    assert "access request" in testbot.pop_message()
    assert "timed out" in testbot.pop_message()
    assert "not approved" in testbot.pop_message()


def get_service_mock():
    service_mock = MagicMock()
    service_mock.get_resource_by_name = MagicMock(return_value = get_mock_resource())
    service_mock.get_account_by_email = MagicMock(return_value = get_mock_resource())
    service_mock.grant_temporary_access = MagicMock()
    return service_mock

def get_mock_resource():
    mock_resource = MagicMock()
    mock_resource.id = 1
    mock_resource.name = "myresource"
    return mock_resource

def get_mock_resource():
    mock_account = MagicMock()
    mock_account.id = 1
    mock_account.name = "myaccount@test.com"
    return mock_account

def get_props_fake():
    return Properties(
        admin_timeout = 1,
        # Default testing bot admin, from config template:
        # https://github.com/errbotio/errbot/blob/master/errbot/config-template.py
        admin = "gbin@localhost", 
        sdm_api_access_key = "access-key",
        sdm_api_secret_key = "secret-key"
    )
