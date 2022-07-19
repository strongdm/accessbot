# pylint: disable=invalid-name
from time import sleep

import pytest
import sys
from unittest.mock import MagicMock

sys.path.append('plugins/sdm')
sys.path.append('e2e')

from test_common import create_config, ErrBotExtraTestSettings, admin_default_email

pytest_plugins = ["errbot.backends.test"]

sdm_email = "sdm@email.com"

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

    def test_whoami_command_when_email_slack_field_disabled(self, mocked_testbot):
        mocked_testbot.push_message("whoami")
        message = mocked_testbot.pop_message()
        assert "person" in message
        assert admin_default_email in message
        assert "SDM email" not in message

    def test_whoami_command_when_email_slack_field_enabled(self, mocked_testbot_with_email_slack_field):
        mocked_testbot_with_email_slack_field.push_message("whoami")
        message = mocked_testbot_with_email_slack_field.pop_message()
        assert "person" in message
        assert admin_default_email in message
        assert "SDM email" in message
        assert sdm_email in message


# pylint: disable=dangerous-default-value
def inject_mocks(testbot, config):
    accessbot = testbot.bot.plugin_manager.plugins['AccessBot']
    accessbot.config = config
    accessbot.get_sdm_email_from_profile = MagicMock(return_value = sdm_email)
    return testbot