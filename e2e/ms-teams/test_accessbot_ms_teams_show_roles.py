# pylint: disable=invalid-name
import pytest
import sys
import re
from unittest.mock import MagicMock

sys.path.append('plugins/sdm')
sys.path.append('e2e')

from lib import ShowRolesHelper
from test_common import create_config, DummyAccount, DummyRole, \
    callback_message_fn, MSTeamsErrBotExtraTestSettings

pytest_plugins = ["errbot.backends.test"]
account_name = "myaccount@test.com"
account_roles_tag = 'sdm-roles'

class Test_show_roles(MSTeamsErrBotExtraTestSettings):
    @pytest.fixture
    def mocked_testbot(self, testbot):
        config = create_config()
        return inject_mocks(testbot, config)

    def test_fail_show_roles_command_when_sent_via_dm(self, mocked_testbot):
        mocked_testbot.push_message("show available roles")
        assert "cannot execute this command via DM" in mocked_testbot.pop_message()

    def test_show_resources_command_when_sent_via_team(self, mocked_testbot):
        mocked_testbot._bot.callback_message = MagicMock(side_effect=callback_message_fn(
            mocked_testbot._bot,
            from_email=account_name,
            approver_is_admin=True
        ))
        mocked_testbot.push_message("show available roles")
        message = mocked_testbot.pop_message()
        assert "Aaa" in message
        assert "Bbb" in message

class Test_not_allowed_by_tag(MSTeamsErrBotExtraTestSettings):
    @pytest.fixture
    def mocked_testbot(self, testbot):
        config = create_config()
        config['USER_ROLES_TAG'] = account_roles_tag
        return inject_mocks(testbot, config, roles = [DummyRole("Bbb", {}), DummyRole("Aaa", {})], account_permitted_roles=['Aaa'])

    def test_show_roles_command(self, mocked_testbot):
        mocked_testbot._bot.callback_message = MagicMock(side_effect=callback_message_fn(
            mocked_testbot._bot,
            from_email=account_name,
            approver_is_admin=True
        ))
        mocked_testbot.push_message("show available roles")
        message = mocked_testbot.pop_message()
        # For some reason we cannot assert the text enclosed between stars
        assert "Aaa" in message
        assert "~~Bbb~~ (not allowed)" in message

def default_dummy_roles():
    return [ DummyRole("Bbb", {}), DummyRole("Aaa", {}) ]

# pylint: disable=dangerous-default-value
def inject_mocks(testbot, config, roles = default_dummy_roles(), account_permitted_roles = None):
    accessbot = testbot.bot.plugin_manager.plugins['AccessBot']
    accessbot.config = config
    accessbot.get_admins = MagicMock(return_value = ["gbin@localhost"])
    accessbot.get_api_access_key = MagicMock(return_value = "api-access_key")
    accessbot.get_api_secret_key = MagicMock(return_value = "c2VjcmV0LWtleQ==") # valid base64 string
    accessbot.get_sdm_service = MagicMock(return_value = create_sdm_service_mock(roles, account_permitted_roles))
    accessbot.get_show_roles_helper = MagicMock(return_value = ShowRolesHelper(accessbot))
    accessbot._bot.azure_active_directory_is_configured = MagicMock(return_value = False)
    return testbot

def create_sdm_service_mock(roles, account_permitted_roles):
    service_mock = MagicMock()
    service_mock.get_all_roles = MagicMock(return_value = roles)
    service_mock.get_account_by_email = MagicMock(return_value = DummyAccount('user', {account_roles_tag: account_permitted_roles}))
    return service_mock
