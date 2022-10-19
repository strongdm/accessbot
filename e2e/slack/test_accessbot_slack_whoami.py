# pylint: disable=invalid-name
import pytest
import sys
from unittest.mock import MagicMock

sys.path.append('plugins/sdm')
sys.path.append('e2e')

from test_common import create_config, ErrBotExtraTestSettings, admin_default_email, DummyAccount

pytest_plugins = ["errbot.backends.test"]

override_email = "override@email.com"
sdm_email = "sdm@email.com"
sdm_email_with_subaddress = "sdm+01@email.com"
email_with_subaddress = "gbin+01@localhost"

class Test_whoami(ErrBotExtraTestSettings):
    @pytest.fixture
    def mocked_testbot(self, testbot):
        config = create_config()
        return inject_mocks(testbot, config)

    @pytest.fixture
    def mocked_testbot_with_email_slack_field(self, testbot):
        config = create_config()
        config['EMAIL_SLACK_FIELD'] = 'sdm email'
        testbot.bot.plugin_manager.plugins['AccessBot'].get_sdm_email_from_profile = MagicMock(return_value=sdm_email)
        return inject_mocks(testbot, config)

    @pytest.fixture
    def mocked_testbot_with_email_override(self, testbot):
        config = create_config()
        mocked_testbot = inject_mocks(testbot, config)
        mocked_testbot.bot.plugin_manager.plugins['AccessBot'].config['SENDER_EMAIL_OVERRIDE'] = override_email
        return mocked_testbot

    @pytest.fixture
    def mocked_testbot_with_email_subaddress(self, testbot):
        config = create_config()
        config['EMAIL_SUBADDRESS'] = '01'
        testbot.bot.sender._email = admin_default_email
        return inject_mocks(testbot, config)

    @pytest.fixture
    def mocked_testbot_with_all_email_features(self, testbot):
        config = create_config()
        config['EMAIL_SLACK_FIELD'] = 'sdm email'
        config['EMAIL_SUBADDRESS'] = '01'
        testbot.bot.sender._email = admin_default_email
        mocked_testbot = inject_mocks(testbot, config)
        mocked_testbot.bot.plugin_manager.plugins['AccessBot'].config['SENDER_EMAIL_OVERRIDE'] = override_email
        return mocked_testbot

    @pytest.fixture
    def mocked_testbot_with_sdm_account_tags(self, testbot):
        config = create_config()
        return inject_mocks(testbot, config, sdm_account=DummyAccount(override_email, {'tagA': 'valueA', 'tagB': 'valueB'}))

    def test_whoami_command_when_email_slack_field_disabled(self, mocked_testbot):
        mocked_testbot.push_message("whoami")
        message = mocked_testbot.pop_message()
        assert "person" in message
        assert admin_default_email in message

    def test_whoami_command_when_email_slack_field_enabled(self, mocked_testbot_with_email_slack_field):
        mocked_testbot_with_email_slack_field.push_message("whoami")
        message = mocked_testbot_with_email_slack_field.pop_message()
        assert "person" in message
        assert sdm_email in message

    def test_whoami_command_when_override_email_enabled(self, mocked_testbot_with_email_override):
        mocked_testbot_with_email_override.push_message("whoami")
        message = mocked_testbot_with_email_override.pop_message()
        assert "person" in message
        assert override_email in message

    def test_whoami_command_when_email_subaddress_enabled(self, mocked_testbot_with_email_subaddress):
        mocked_testbot_with_email_subaddress.push_message("whoami")
        message = mocked_testbot_with_email_subaddress.pop_message()
        assert "person" in message
        assert email_with_subaddress in message

    def test_whoami_command_when_all_email_features_enabled(self, mocked_testbot_with_all_email_features):
        accessbot = mocked_testbot_with_all_email_features.bot.plugin_manager.plugins['AccessBot']
        mocked_testbot_with_all_email_features.push_message("whoami")
        message = mocked_testbot_with_all_email_features.pop_message()
        assert "person" in message
        assert override_email in message
        accessbot.config['SENDER_EMAIL_OVERRIDE'] = None
        mocked_testbot_with_all_email_features.push_message("whoami")
        message = mocked_testbot_with_all_email_features.pop_message()
        assert sdm_email_with_subaddress in message
        accessbot.config['EMAIL_SLACK_FIELD'] = None
        mocked_testbot_with_all_email_features.push_message("whoami")
        message = mocked_testbot_with_all_email_features.pop_message()
        assert email_with_subaddress in message
        accessbot.config['EMAIL_SUBADDRESS'] = None
        mocked_testbot_with_all_email_features.push_message("whoami")
        message = mocked_testbot_with_all_email_features.pop_message()
        assert admin_default_email in message

    def test_whoami_command_when_sdm_account_has_tags(self, mocked_testbot_with_sdm_account_tags):
        mocked_testbot_with_sdm_account_tags.push_message("whoami")
        message = mocked_testbot_with_sdm_account_tags.pop_message()
        assert "SDM Account tags" in message
        assert 'tagA: valueA' in message
        assert 'tagB: valueB' in message


# pylint: disable=dangerous-default-value
def inject_mocks(testbot, config, sdm_account=None):
    accessbot = testbot.bot.plugin_manager.plugins['AccessBot']
    config['SENDER_EMAIL_OVERRIDE'] = None
    accessbot.config = config
    accessbot.get_sdm_email_from_profile = MagicMock(return_value=sdm_email)
    accessbot.get_sdm_account = MagicMock(return_value=sdm_account)
    return testbot
