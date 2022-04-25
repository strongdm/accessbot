# pylint: disable=invalid-name
import sys
import pytest
from unittest.mock import MagicMock

sys.path.append('plugins/sdm')
sys.path.append('e2e')

from test_common import create_config, get_dummy_person, ErrBotExtraTestSettings

pytest_plugins = ["errbot.backends.test"]

def mocked_get_bot_admins():
    return ['@bot_admin']

class Test_update_access_control_admins(ErrBotExtraTestSettings):
    bot_admins = ['@bot_admin']
    admins_channel = '#admin-channel'
    extra_config = {
        **ErrBotExtraTestSettings.extra_config,
        'BOT_ADMINS': bot_admins,
        'get_bot_admins': MagicMock(side_effect = mocked_get_bot_admins),
        'ACCESS_CONTROLS': {
            '*': {
                'allowusers': bot_admins,
                'allowrooms': [admins_channel],
                'allowmuc': True,
            }
        }
    }

    @pytest.fixture
    def mocked_testbot(self, testbot):
        config = create_config()
        config['ADMINS_CHANNEL'] = self.admins_channel
        config['ADMINS_CHANNEL_ELEVATE'] = True
        return inject_config(testbot, config)

    def test_update_admins_when_admins_channel_is_configured(self, mocked_testbot):
        mocked_testbot.bot.plugin_manager.plugins['AccessBot'].update_access_control_admins()
        assert len(mocked_testbot._bot.bot_config.ACCESS_CONTROLS['*']['allowusers']) == len(get_dummy_members())
        assert len(mocked_testbot._bot.bot_config.ACCESS_CONTROLS['*']['allowrooms']) == 1
        assert mocked_testbot._bot.bot_config.ACCESS_CONTROLS['*']['allowrooms'][0] == self.admins_channel

    def test_clean_admins_when_disabling_admins_channel_elevate(self, mocked_testbot):
        mocked_testbot.bot.plugin_manager.plugins['AccessBot'].update_access_control_admins()
        mocked_testbot.bot.plugin_manager.plugins['AccessBot'].config['ADMINS_CHANNEL_ELEVATE'] = False
        mocked_testbot.bot.plugin_manager.plugins['AccessBot'].update_access_control_admins()
        assert len(mocked_testbot._bot.bot_config.ACCESS_CONTROLS['*']['allowusers']) == 1
        assert len(mocked_testbot._bot.bot_config.ACCESS_CONTROLS['*']['allowrooms']) == 0

def inject_config(testbot, config):
    accessbot = testbot.bot.plugin_manager.plugins['AccessBot']
    accessbot.config = config
    accessbot.build_identifier = MagicMock(
        side_effect=mocked_build_identifier
    )
    accessbot._bot.conversations_members = MagicMock(return_value = get_dummy_members())
    accessbot._bot.userid_to_username = MagicMock(side_effect = mocked_userid_to_username)
    return testbot

def mocked_build_identifier(param):
    return get_dummy_person(param)

def mocked_userid_to_username(param):
    return f'{param}'

def get_dummy_members():
    return [
        'bot_admin',
        'channel_admin1',
        'channel_admin2'
    ]
