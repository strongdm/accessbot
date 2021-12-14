# pylint: disable=invalid-name
import time
import pytest
import sys
from unittest.mock import MagicMock
from slack_sdk.errors import SlackApiError

sys.path.append('plugins/sdm')
sys.path.append('e2e/')

from test_common import create_config, DummyAccount, DummyRole, get_rate_limited_slack_response_error
from lib import ShowRolesHelper

pytest_plugins = ["errbot.backends.test"]
extra_plugin_dir = "plugins/sdm"
account_name = "myaccount@test.com"
account_roles_tag = 'sdm-roles'

class Test_show_roles:
    @pytest.fixture
    def mocked_testbot(self, testbot):
        config = create_config()
        return inject_mocks(testbot, config)

    def test_show_roles_command(self, mocked_testbot):
        mocked_testbot.push_message("show available roles")
        message = mocked_testbot.pop_message()
        assert "Aaa" in message
        assert "Bbb" in message

class Test_show_roles_except_hidden_roles:
    @pytest.fixture
    def mocked_testbot(self, testbot):
        config = create_config()
        config['HIDE_ROLE_TAG'] = 'hide-role'
        return inject_mocks(testbot, config, roles=[DummyRole("Bbb", {}), DummyRole("Aaa", {'hide-role': 'true'})])

    def test_show_roles_command(self, mocked_testbot):
        mocked_testbot.push_message("show available roles")
        message = mocked_testbot.pop_message()
        assert "Aaa" not in message
        assert "Bbb" in message

class Test_auto_approve_by_tag:
    @pytest.fixture
    def mocked_testbot(self, testbot):
        config = create_config()
        config['AUTO_APPROVE_ROLE_TAG'] = 'auto-approve-role'
        return inject_mocks(testbot, config, roles = [DummyRole("Bbb", {}), DummyRole("Aaa", {'auto-approve-role': 'true'})])

    def test_show_roles_command(self, mocked_testbot):
        mocked_testbot.push_message("show available roles")
        message = mocked_testbot.pop_message()
        # For some reason we cannot assert the text enclosed between stars
        assert "Aaa (auto-approve)" in message
        assert "Bbb" in message

class Test_not_allowed_by_tag:
    @pytest.fixture
    def mocked_testbot(self, testbot):
        config = create_config()
        config['USER_ROLES_TAG'] = account_roles_tag
        return inject_mocks(testbot, config, roles = [DummyRole("Bbb", {}), DummyRole("Aaa", {})], account_permitted_roles=['Aaa'])

    def test_show_roles_command(self, mocked_testbot):
        mocked_testbot.push_message("show available roles")
        message = mocked_testbot.pop_message()
        # For some reason we cannot assert the text enclosed between stars
        assert "Aaa" in message
        assert "~Bbb~ (not allowed)" in message

class Test_alternative_email:
    alternative_email_tag = 'alternative-email'

    @pytest.fixture
    def mocked_user_profile(self):
        return {
            'fields': {
                'XXX': {
                    'label': self.alternative_email_tag,
                    'value': account_name,
                }
            }
        }

    @pytest.fixture
    def mocked_testbot_with_profile(self, testbot, mocked_user_profile):
        config = create_config()
        config['SENDER_EMAIL_OVERRIDE'] = None
        config['EMAIL_SLACK_FIELD'] = self.alternative_email_tag
        testbot.bot.sender.userid = 'XXX'
        testbot.bot.find_user_profile = MagicMock(return_value=mocked_user_profile)
        return inject_mocks(testbot, config)

    @pytest.fixture
    def mocked_testbot_with_ratelimited_error(self, testbot):
        config = create_config()
        config['SENDER_EMAIL_OVERRIDE'] = None
        config['EMAIL_SLACK_FIELD'] = self.alternative_email_tag
        testbot.bot.sender.userid = 'XXX'
        testbot.bot.find_user_profile = MagicMock(side_effect=get_rate_limited_slack_response_error())
        return inject_mocks(testbot, config)

    def test_when_has_profile(self, mocked_testbot_with_profile):
        mocked_testbot_with_profile.push_message("show available roles")
        message = mocked_testbot_with_profile.pop_message()
        assert "Aaa" in message
        assert "Bbb" in message

    def test_when_throws_ratelimited_error(self, mocked_testbot_with_ratelimited_error):
        mocked_testbot_with_ratelimited_error.push_message("show available roles")
        message = mocked_testbot_with_ratelimited_error.pop_message()
        assert "An error occurred" in message
        assert "Too many requests were made" in message



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
    return testbot

def create_sdm_service_mock(roles, account_permitted_roles):
    service_mock = MagicMock()
    service_mock.get_all_roles = MagicMock(return_value = roles)
    service_mock.get_account_by_email = MagicMock(return_value = DummyAccount('user', {account_roles_tag: account_permitted_roles}))
    return service_mock
