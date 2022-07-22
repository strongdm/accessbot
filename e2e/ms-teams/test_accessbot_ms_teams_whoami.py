# pylint: disable=invalid-name
import pytest
import sys

sys.path.append('plugins/sdm')
sys.path.append('e2e')

from test_common import create_config, ErrBotExtraTestSettings, admin_default_email

pytest_plugins = ["errbot.backends.test"]

override_email = "override@email.com"
email_with_subaddress = "gbin+01@localhost"

class Test_whoami(ErrBotExtraTestSettings):
    @pytest.fixture
    def mocked_testbot(self, testbot):
        config = create_config()
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
        config['EMAIL_SUBADDRESS'] = '01'
        testbot.bot.sender._email = admin_default_email
        mocked_testbot = inject_mocks(testbot, config)
        mocked_testbot.bot.plugin_manager.plugins['AccessBot'].config['SENDER_EMAIL_OVERRIDE'] = override_email
        return mocked_testbot

    def test_whoami_command_when_and_override_email_enabled(self, mocked_testbot_with_email_override):
        mocked_testbot_with_email_override.push_message("whoami")
        message = mocked_testbot_with_email_override.pop_message()
        assert "person" in message
        assert override_email in message

    def test_whoami_command_when_and_email_subaddress_enabled(self, mocked_testbot_with_email_subaddress):
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
        assert email_with_subaddress in message
        accessbot.config['EMAIL_SUBADDRESS'] = None
        mocked_testbot_with_all_email_features.push_message("whoami")
        message = mocked_testbot_with_all_email_features.pop_message()
        assert admin_default_email in message


# pylint: disable=dangerous-default-value
def inject_mocks(testbot, config):
    accessbot = testbot.bot.plugin_manager.plugins['AccessBot']
    config['SENDER_EMAIL_OVERRIDE'] = None
    accessbot.config = config
    return testbot
