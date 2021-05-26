# pylint: disable=invalid-name
import pytest
import sys
from unittest.mock import MagicMock

from test_common import create_config, DummyResource
sys.path.append('plugins/sdm')
from lib import ApproveHelper, GrantHelper, PollerHelper

pytest_plugins = ["errbot.backends.test"]
extra_plugin_dir = 'plugins/sdm'

role_id = 111
role_name = "role-name"
account_id = 1
account_name = "myaccount@test.com"
access_request_id = "12ab"

class Test_assign_role:
    @pytest.fixture
    def mocked_testbot(self, testbot):
        config = create_config()
        return inject_mocks(testbot, config)

    def test_show_resources_command(self, mocked_testbot):
        mocked_testbot.push_message(f"access to role {role_name}")
        mocked_testbot.push_message(f"yes {access_request_id}")
        assert "valid request" in mocked_testbot.pop_message()
        assert "assign request" in mocked_testbot.pop_message()
        assert "Assigning" in mocked_testbot.pop_message()


# pylint: disable=dangerous-default-value
def inject_mocks(testbot, config):
    accessbot = testbot.bot.plugin_manager.plugins['AccessBot']
    accessbot.config = config
    accessbot.start_poller(0.5, PollerHelper(accessbot).stale_grant_requests_cleaner)
    accessbot.get_admins = MagicMock(return_value = ["gbin@localhost"])
    accessbot.get_api_access_key = MagicMock(return_value = "api-access_key")
    accessbot.get_api_secret_key = MagicMock(return_value = "c2VjcmV0LWtleQ==") # valid base64 string
    accessbot.get_sdm_service = MagicMock(return_value = create_sdm_service_mock())
    accessbot.get_grant_helper = MagicMock(return_value = create_grant_helper(accessbot))
    accessbot.get_approve_helper = MagicMock(return_value = create_approve_helper(accessbot))
    return testbot

def create_grant_helper(accessbot):
    helper = GrantHelper(accessbot)
    helper.generate_grant_request_id = MagicMock(return_value = access_request_id)
    return helper

def create_approve_helper(accessbot):
    return ApproveHelper(accessbot)

def create_sdm_service_mock():
    service_mock = MagicMock()
    service_mock.get_account_by_email = MagicMock(return_value = create_mock_account())
    service_mock.get_role_by_name = MagicMock(return_value = create_mock_role())
    return service_mock

def create_mock_account():
    mock_account = MagicMock()
    mock_account.id = account_id
    mock_account.name = account_name
    return mock_account

def create_mock_role():
    mock_role = MagicMock()
    mock_role.id = role_id
    mock_role.name = role_name
    return mock_role
