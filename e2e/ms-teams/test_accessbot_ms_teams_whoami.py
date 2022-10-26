# pylint: disable=invalid-name
from unittest.mock import MagicMock

import pytest
import sys

sys.path.append('plugins/sdm')
sys.path.append('e2e')
sys.path.append('errbot-backend-botframework')

from test_common import create_config, MSTeamsErrBotExtraTestSettings, admin_default_email, DummyAccount, \
    callback_message_fn
from botframework import ChannelIdentifier, Identifier

pytest_plugins = ["errbot.backends.test"]

override_email = "override@email.com"
email_with_subaddress = "gbin+01@localhost"
alternative_email = "other@email.com"

class Test_whoami(MSTeamsErrBotExtraTestSettings):
    @pytest.fixture
    def mocked_testbot_with_sdm_account_tags(self, testbot):
        config = create_config()
        return inject_mocks(testbot, config, sdm_account=DummyAccount(override_email, {'tagA': 'valueA', 'tagB': 'valueB'}))

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

    @pytest.fixture
    def mocked_testbot_with_alternative_emails(self, testbot):
        config = create_config()
        testbot._bot.callback_message = MagicMock(side_effect=callback_message_fn(
            testbot._bot
        ))
        testbot._bot.build_identifier = MagicMock(return_value=get_mocked_identifier())
        return inject_mocks(testbot, config, use_alternative_emails=True, alternative_emails=[alternative_email])

    def test_whoami_command_when_and_override_email_enabled(self, mocked_testbot_with_email_override):
        mocked_testbot_with_email_override.push_message("whoami")
        message = mocked_testbot_with_email_override.pop_message()
        assert "email" in message
        assert override_email in message

    def test_whoami_command_when_and_email_subaddress_enabled(self, mocked_testbot_with_email_subaddress):
        mocked_testbot_with_email_subaddress.push_message("whoami")
        message = mocked_testbot_with_email_subaddress.pop_message()
        assert "email" in message
        assert email_with_subaddress in message

    def test_whoami_command_when_all_email_features_enabled(self, mocked_testbot_with_all_email_features):
        accessbot = mocked_testbot_with_all_email_features.bot.plugin_manager.plugins['AccessBot']
        mocked_testbot_with_all_email_features.push_message("whoami")
        message = mocked_testbot_with_all_email_features.pop_message()
        assert "email" in message
        assert override_email in message
        accessbot.config['SENDER_EMAIL_OVERRIDE'] = None
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
        assert "tagA: valueA" in message
        assert "tagB: valueB" in message

    def test_whoami_command_when_alternative_emails_is_enabled(self, mocked_testbot_with_alternative_emails):
        mocked_testbot_with_alternative_emails.push_message("whoami")
        message = mocked_testbot_with_alternative_emails.pop_message()
        assert "Azure AD alternative emails" in message
        assert alternative_email in message


# pylint: disable=dangerous-default-value
def inject_mocks(testbot, config, sdm_account=None, use_alternative_emails=False, alternative_emails=[]):
    accessbot = testbot.bot.plugin_manager.plugins['AccessBot']
    config['SENDER_EMAIL_OVERRIDE'] = None
    accessbot.config = config
    accessbot.get_sdm_account = MagicMock(return_value=sdm_account)
    accessbot._bot.azure_active_directory_is_configured = MagicMock(return_value=use_alternative_emails)
    accessbot._bot.get_other_emails_by_aad_id = MagicMock(return_value=alternative_emails)
    return testbot

def get_mocked_identifier():
    identifier = Identifier({
        'room': ChannelIdentifier(
            {
                'id': '19:ccc',
                'displayName': 'channel',
                'team': {'id': '19:ttt', 'displayName': 'team'}
            }
        )
    })
    return identifier
