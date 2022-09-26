# pylint: disable=invalid-name
import sys
import time
import datetime
import pytest
from unittest.mock import MagicMock, patch

sys.path.append('plugins/sdm')
sys.path.append('e2e')

from test_common import create_config, callback_message_fn, MSTeamsErrBotExtraTestSettings
from lib import ApproveHelper, RoleGrantHelper

pytest_plugins = ["errbot.backends.test"]

role_id = 111
role_name = "role-name"
resource_id = 1
resource_name = "myresource"
account_id = 1
account_name = "myaccount@test.com"
access_request_id = "12AB"

class Test_assign_role(MSTeamsErrBotExtraTestSettings):
    @pytest.fixture
    def mocked_testbot(self, testbot):
        config = create_config()
        return inject_mocks(testbot, config)

    class NewDate(datetime.datetime):
        @classmethod
        def now(cls, tz=None):
            return cls(2021, 5, 12)

    def test_fail_assign_role_command_when_sent_via_dm(self, mocked_testbot):
        mocked_testbot.push_message(f"access to role {role_name}")
        assert "cannot execute this command via DM" in mocked_testbot.pop_message()

    def test_assign_role_command(self, mocked_testbot):
        accessbot = mocked_testbot.bot.plugin_manager.plugins['AccessBot']
        mocked_testbot._bot.callback_message = callback_message_fn(mocked_testbot._bot)
        grant_temporary_access_mock = accessbot.get_sdm_service().grant_temporary_access
        with patch('datetime.datetime', new = self.NewDate):
            mocked_testbot.push_message(f"access to role {role_name}")
            mocked_testbot.push_message(f"yes {access_request_id}")
            assert "valid request" in mocked_testbot.pop_message()
            assert "assign request" in mocked_testbot.pop_message()
            assert "Granting" in mocked_testbot.pop_message()

            start_from = datetime.datetime(2021, 5, 12, 0, 0)
            valid_until = datetime.datetime(2021, 5, 12, 1, 0)
            grant_temporary_access_mock.assert_called_with(resource_id, account_id, start_from, valid_until)

    def test_assign_role_command_when_not_self_approved(self, mocked_testbot):
        accessbot = mocked_testbot.bot.plugin_manager.plugins['AccessBot']
        mocked_testbot._bot.callback_message = callback_message_fn(mocked_testbot._bot, from_email=account_name, approver_is_admin=True)
        grant_temporary_access_mock = accessbot.get_sdm_service().grant_temporary_access
        with patch('datetime.datetime', new = self.NewDate):
            mocked_testbot.push_message(f"access to role {role_name}")
            mocked_testbot.push_message(f"yes {access_request_id}")
            assert "valid request" in mocked_testbot.pop_message()
            assert "assign request" in mocked_testbot.pop_message()
            assert "Granting" in mocked_testbot.pop_message()

            start_from = datetime.datetime(2021, 5, 12, 0, 0)
            valid_until = datetime.datetime(2021, 5, 12, 1, 0)
            grant_temporary_access_mock.assert_called_with(resource_id, account_id, start_from, valid_until)

    def test_fail_assign_role_command_when_self_approved(self, mocked_testbot):
        accessbot = mocked_testbot.bot.plugin_manager.plugins['AccessBot']
        mocked_testbot._bot.callback_message = callback_message_fn(mocked_testbot._bot, from_email=account_name)
        with patch('datetime.datetime', new = self.NewDate):
            mocked_testbot.push_message(f"access to role {role_name}")
            mocked_testbot.push_message(f"yes {access_request_id}")
            assert "valid request" in mocked_testbot.pop_message()
            assert "assign request" in mocked_testbot.pop_message()
            assert "not an admin to self approve" in mocked_testbot.pop_message()

# pylint: disable=dangerous-default-value
def inject_mocks(testbot, config, roles = [], account_tags = None, role_tags = None):
    accessbot = testbot.bot.plugin_manager.plugins['AccessBot']
    accessbot.config = config
    accessbot.get_admins = MagicMock(return_value = ["gbin@localhost"])
    accessbot.get_api_access_key = MagicMock(return_value = "api-access_key")
    accessbot.get_api_secret_key = MagicMock(return_value = "c2VjcmV0LWtleQ==") # valid base64 string
    accessbot.get_sdm_service = MagicMock(return_value = create_sdm_service_mock(roles, account_tags, role_tags))
    accessbot.get_role_grant_helper = MagicMock(return_value = create_role_grant_helper(accessbot))
    accessbot.get_approve_helper = MagicMock(return_value = create_approve_helper(accessbot))
    accessbot._bot.azure_active_directory_is_configured = MagicMock(return_value = False)
    return testbot

def create_role_grant_helper(accessbot):
    helper = RoleGrantHelper(accessbot)
    helper.generate_grant_request_id = MagicMock(return_value = access_request_id)
    return helper

def create_approve_helper(accessbot):
    return ApproveHelper(accessbot)

def create_sdm_service_mock(roles, account_tags, role_tags):
    service_mock = MagicMock()
    service_mock.get_role_by_name = MagicMock(return_value = create_mock_role(role_tags))
    service_mock.get_account_by_email = MagicMock(return_value = create_mock_account(account_tags))
    service_mock.get_all_resources_by_role = MagicMock(return_value = create_mock_resources())
    service_mock.account_grant_exists = MagicMock(return_value = False)
    service_mock.get_all_roles = MagicMock(return_value = roles)
    return service_mock

def create_mock_account(tags):
    mock_account = MagicMock()
    mock_account.id = account_id
    mock_account.name = account_name
    mock_account.email = account_name
    mock_account.tags = tags
    return mock_account

def create_mock_role(tags):
    mock_role = MagicMock()
    mock_role.id = role_id
    mock_role.name = role_name
    mock_role.tags = tags
    return mock_role

def create_mock_resources():
    mock_resource = MagicMock()
    mock_resource.id = resource_id
    mock_resource.name = resource_name
    return [mock_resource]
