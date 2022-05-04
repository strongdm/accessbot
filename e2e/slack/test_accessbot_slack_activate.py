# pylint: disable=invalid-name
import sys
from time import sleep

import pytest
from unittest.mock import MagicMock

sys.path.append('plugins/sdm')
sys.path.append('e2e')

from test_common import create_config, get_dummy_person, ErrBotExtraTestSettings, callback_message_fn

pytest_plugins = ["errbot.backends.test"]

def mocked_get_bot_admins():
    return ['@bot_admin']

class Test_update_access_control_admins(ErrBotExtraTestSettings):
    bot_admins = ['@bot_admin']
    admins_channel = 'admin-channel'
    extra_config = {
        **ErrBotExtraTestSettings.extra_config,
        'BOT_ADMINS': bot_admins,
        'get_bot_admins': MagicMock(side_effect = mocked_get_bot_admins),
        'ACCESS_CONTROLS': {
            '*': {
                'allowusers': bot_admins,
                'allowrooms': [f'#{admins_channel}'],
                'allowmuc': True,
            }
        }
    }

    @pytest.fixture
    def mocked_testbot(self, testbot):
        config = create_config()
        config['ADMINS_CHANNEL'] = f'#{self.admins_channel}'
        config['ADMINS_CHANNEL_ELEVATE'] = True
        return inject_config(testbot, config)

    def test_update_admins_when_admins_channel_is_configured(self, mocked_testbot):
        mocked_testbot.bot.plugin_manager.plugins['AccessBot'].update_access_control_admins()
        assert len(mocked_testbot._bot.bot_config.ACCESS_CONTROLS['*']['allowusers']) == len(get_dummy_members())
        assert len(mocked_testbot._bot.bot_config.ACCESS_CONTROLS['*']['allowrooms']) == 1
        assert mocked_testbot._bot.bot_config.ACCESS_CONTROLS['*']['allowrooms'][0] == f'#{self.admins_channel}'

    def test_clean_admins_when_disabling_admins_channel_elevate(self, mocked_testbot):
        mocked_testbot.bot.plugin_manager.plugins['AccessBot'].update_access_control_admins()
        mocked_testbot.bot.plugin_manager.plugins['AccessBot'].config['ADMINS_CHANNEL_ELEVATE'] = False
        mocked_testbot.bot.plugin_manager.plugins['AccessBot'].update_access_control_admins()
        assert len(mocked_testbot._bot.bot_config.ACCESS_CONTROLS['*']['allowusers']) == 1
        assert len(mocked_testbot._bot.bot_config.ACCESS_CONTROLS['*']['allowrooms']) == 0

    def test_elevate_admin_user_when_entering_in_admins_channel(self, mocked_testbot):
        assert len(mocked_testbot._bot.bot_config.ACCESS_CONTROLS['*']['allowusers']) == 1
        mocked_testbot._bot.callback_message = MagicMock(side_effect=callback_message_fn(
            mocked_testbot._bot,
            from_username="new_bot_admin",
            room_name=self.admins_channel,
            check_elevate_admin_user=True,
        ))
        mocked_testbot.push_message("hello world!")
        sleep(0.1)
        assert len(mocked_testbot._bot.bot_config.BOT_ADMINS) == 2

    def test_remove_admin_status_after_leaving_admins_channel(self, mocked_testbot):
        mocked_testbot._bot.bot_config.BOT_ADMINS.append("@new_bot_admin")
        assert len(mocked_testbot._bot.bot_config.BOT_ADMINS) == 2
        mocked_testbot._bot.callback_message = MagicMock(side_effect=callback_message_fn(
            mocked_testbot._bot,
            from_username="new_bot_admin",
            from_userid="new_bot_admin",
            check_elevate_admin_user=True,
        ))
        mocked_testbot.push_message("hello world!")
        sleep(0.1)
        assert len(mocked_testbot._bot.bot_config.BOT_ADMINS) == 1

def inject_config(testbot, config):
    accessbot = testbot.bot.plugin_manager.plugins['AccessBot']
    accessbot.config = config
    accessbot.build_identifier = MagicMock(
        side_effect=mocked_build_identifier
    )
    accessbot._bot.conversation_members = MagicMock(return_value = get_dummy_members())
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
