# pylint: disable=invalid-name
import datetime
import pytest
import sys
import time
from unittest.mock import MagicMock, patch

from test_common import create_config, DummyResource
sys.path.append('plugins/sdm')
from lib import ApproveHelper, GrantHelper, PollerHelper

pytest_plugins = ["errbot.backends.test"]
extra_plugin_dir = 'plugins/sdm'

role_id = 111
role_name = "role-name"
resource_id = 1
resource_name = "myresource"
account_id = 1
account_name = "myaccount@test.com"
access_request_id = "12ab"

class Test_assign_role:
    @pytest.fixture
    def mocked_testbot(self, testbot):
        config = create_config()
        return inject_mocks(testbot, config)

    class NewDate(datetime.datetime):
        @classmethod
        def now(cls, tz=None):
            return cls(2021, 5, 12)

    def test_assign_role_command(self, mocked_testbot):
        accessbot = mocked_testbot.bot.plugin_manager.plugins['AccessBot']
        grant_temporary_access_mock = accessbot.get_sdm_service().grant_temporary_access
        with patch('datetime.datetime', new = self.NewDate):
            push_access_role_request(mocked_testbot)
            mocked_testbot.push_message(f"yes {access_request_id}")
            assert "valid request" in mocked_testbot.pop_message()
            assert "assign request" in mocked_testbot.pop_message()
            assert "Granting" in mocked_testbot.pop_message()

            start_from = datetime.datetime(2021, 5, 12, 0, 0)
            valid_until = datetime.datetime(2021, 5, 12, 1, 0)
            grant_temporary_access_mock.assert_called_with(resource_id, account_id, start_from, valid_until)


# pylint: disable=dangerous-default-value
def inject_mocks(testbot, config):
    accessbot = testbot.bot.plugin_manager.plugins['AccessBot']
    accessbot.config = config
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
    service_mock.get_all_resources_by_role = MagicMock(return_value = create_mock_resources())
    service_mock.grant_exists = MagicMock(return_value = False)
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

def create_mock_resources():
    mock_resource = MagicMock()
    mock_resource.id = resource_id
    mock_resource.name = resource_name
    return [mock_resource]

def push_access_role_request(testbot):
    testbot.push_message(f"access to role {role_name}")
    # gives some time to process
    # needed in slow environments, e.g. github actions
    time.sleep(0.2)
