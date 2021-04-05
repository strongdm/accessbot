from errbot.backends.base import Message
import pytest
import sys
import time
from unittest.mock import MagicMock

sys.path.append('plugins/sdm')
from access_helper import AccessHelper
import properties 

pytest_plugins = ["errbot.backends.test"]
extra_plugin_dir = 'plugins/sdm'

def test_help_command(testbot):
    testbot.push_message("help")
    assert "access to resource-name" in testbot.pop_message()

@pytest.fixture
def mocked_bot(testbot):
    mock_dict = {'access_helper': create_access_helper()}
    testbot.inject_mocks('AccessBot', mock_dict)
    return testbot

def test_access_command_grant_approved(mocked_bot):
    mocked_bot.push_message("access to Xxx")
    mocked_bot.push_message("yes")
    assert "valid request" in mocked_bot.pop_message()
    assert "access request" in mocked_bot.pop_message()
    assert "Granting" in mocked_bot.pop_message()

def test_access_command_grant_timed_out(mocked_bot):
    mocked_bot.push_message("access to Xxx")
    assert "valid request" in mocked_bot.pop_message()
    assert "access request" in mocked_bot.pop_message()
    assert "timed out" in mocked_bot.pop_message()
    assert "not approved" in mocked_bot.pop_message()

def test_access_command_grant_not_approved(mocked_bot):
    mocked_bot.push_message("access to Xxx")
    mocked_bot.push_message("no") # Anything but yes
    assert "valid request" in mocked_bot.pop_message()
    assert "access request" in mocked_bot.pop_message()
    assert "timed out" in mocked_bot.pop_message()
    assert "not approved" in mocked_bot.pop_message()


def create_access_helper():
    access_helper = AccessHelper(properties.get())
    access_helper.access_service = create_account_service_mock()
    return access_helper

def create_account_service_mock():
    service_mock = MagicMock()
    service_mock.get_resource_by_name = MagicMock(return_value = create_mock_resource())
    service_mock.get_account_by_email = MagicMock(return_value = create_mock_account())
    service_mock.grant_temporary_access = MagicMock()
    return service_mock

def create_mock_resource():
    mock_resource = MagicMock()
    mock_resource.id = 1
    mock_resource.name = "myresource"
    return mock_resource

def create_mock_account():
    mock_account = MagicMock()
    mock_account.id = 1
    mock_account.name = "myaccount@test.com"
    return mock_account
