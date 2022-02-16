import sys
import time
import pytest
from unittest.mock import MagicMock

sys.path.append('plugins/sdm')
sys.path.append('e2e')

from test_common import create_config, callback_message_fn, MSTeamsErrBotExtraTestSettings
from lib import ApproveHelper, ResourceGrantHelper

pytest_plugins = ["errbot.backends.test"]

resource_id = 1
resource_name = "myresource"
account_id = 1
account_name = "myaccount@test.com"
access_request_id = "12ab"

class Test_default_flow(MSTeamsErrBotExtraTestSettings):
    @pytest.fixture
    def mocked_testbot(self, testbot):
        config = create_config()
        return inject_config(testbot, config)

    def test_fail_access_command_when_sent_via_dm(self, mocked_testbot):
        mocked_testbot.push_message("access to Xxx")
        assert "cannot execute this command via DM" in mocked_testbot.pop_message()

    def test_access_command_grant_when_self_approved(self, mocked_testbot):
        mocked_testbot._bot.callback_message = callback_message_fn(mocked_testbot._bot)
        mocked_testbot.push_message("access to Xxx")
        mocked_testbot.push_message(f"yes {access_request_id}")
        assert "valid request" in mocked_testbot.pop_message()
        assert "access request" in mocked_testbot.pop_message()
        assert "Granting" in mocked_testbot.pop_message()

    def test_access_command_grant_approved(self, mocked_testbot):
        mocked_testbot._bot.callback_message = MagicMock(side_effect=callback_message_fn(
            mocked_testbot._bot,
            from_email=account_name,
            approver_is_admin=True
        ))
        mocked_testbot.push_message("access to Xxx")
        mocked_testbot.push_message(f"yes {access_request_id}")
        assert "valid request" in mocked_testbot.pop_message()
        assert "access request" in mocked_testbot.pop_message()
        assert "Granting" in mocked_testbot.pop_message()

    def test_fail_access_command_when_not_admin_self_approved(self, mocked_testbot):
        mocked_testbot._bot.callback_message = MagicMock(side_effect=callback_message_fn(
            mocked_testbot._bot,
            from_email=account_name
        ))
        mocked_testbot.push_message("access to Xxx")
        mocked_testbot.push_message(f"yes {access_request_id}")
        assert "valid request" in mocked_testbot.pop_message()
        assert "access request" in mocked_testbot.pop_message()
        assert "not an admin to self approve" in mocked_testbot.pop_message()

# pylint: disable=dangerous-default-value
def inject_config(testbot, config, admins=["gbin@localhost"], tags={}, resources_by_role=[], account_grant_exists=False, resources=[], alternate_email = False):
    accessbot = testbot.bot.plugin_manager.plugins['AccessBot']
    accessbot.config = config
    accessbot.get_admins = MagicMock(return_value = admins)
    accessbot.get_api_access_key = MagicMock(return_value = "api-access_key")
    accessbot.get_api_secret_key = MagicMock(return_value = "c2VjcmV0LWtleQ==")  # valid base64 string
    accessbot.get_sdm_service = MagicMock(return_value = create_sdm_service_mock(tags, resources_by_role, account_grant_exists, resources))
    accessbot.get_resource_grant_helper = MagicMock(return_value = create_resource_grant_helper(accessbot))
    accessbot.get_approve_helper = MagicMock(return_value = create_approve_helper(accessbot))
    return testbot

def create_resource_grant_helper(accessbot):
    helper = ResourceGrantHelper(accessbot)
    helper.generate_grant_request_id = MagicMock(return_value = access_request_id)
    return helper

def create_approve_helper(accessbot):
    return ApproveHelper(accessbot)

def create_sdm_service_mock(tags, resources_by_role, account_grant_exists, resources):
    mock = MagicMock()
    mock.get_resource_by_name = MagicMock(return_value = create_resource_mock(tags))
    mock.get_account_by_email = MagicMock(return_value = create_account_mock())
    mock.grant_temporary_access = MagicMock()
    mock.get_all_resources_by_role = MagicMock(return_value = resources_by_role)
    mock.account_grant_exists = MagicMock(return_value = account_grant_exists)
    mock.get_all_resources = MagicMock(return_value = resources)
    return mock

def create_resource_mock(tags):
    mock = MagicMock()
    mock.id = resource_id
    mock.name = resource_name
    mock.tags = tags
    return mock

def create_account_mock(account_email = account_name):
    mock = MagicMock()
    mock.id = account_id
    mock.name = account_name
    mock.email = account_email
    return mock

def create_approver_mock(account_email = account_name):
    mock = MagicMock()
    mock.email = account_email
    mock.nick = account_email
    return mock
