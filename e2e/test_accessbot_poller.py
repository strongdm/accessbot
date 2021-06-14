# pylint: disable=invalid-name
import os
import pytest
import sys
import time
from errbot.backends.base import Message
from unittest.mock import MagicMock

from test_common import create_config, send_message_override
sys.path.append('plugins/sdm')
from lib import PollerHelper

pytest_plugins = ["errbot.backends.test"]
extra_plugin_dir = 'plugins/sdm'

access_request_id = "12ab"

class Test_stale_grant_requests_cleaner:
    sdm_admin = "gbin@localhost"
    channel_name = 'testroom'
    raw_messages = []

    @pytest.fixture
    def mocked_testbot(self, testbot):
        self.raw_messages = []
        testbot.bot.send_message = send_message_override(testbot.bot, self.raw_messages)
        config = create_config()
        config['ADMIN_TIMEOUT'] = 0
        accessbot = testbot.bot.plugin_manager.plugins['AccessBot']
        accessbot.config = config
        return testbot

        
    def test_when_handling_direct_messages(self, mocked_testbot):
        os.environ['SDM_ADMINS'] = self.sdm_admin

        accessbot = mocked_testbot.bot.plugin_manager.plugins['AccessBot']
        sender_id = accessbot.build_identifier(accessbot.config['SENDER_EMAIL_OVERRIDE'])
        accessbot.enter_grant_request(access_request_id, Message(frm = sender_id), MagicMock(), MagicMock(), MagicMock())
        assert access_request_id in accessbot.get_grant_request_ids()

        PollerHelper(accessbot).stale_grant_requests_cleaner()

        assert access_request_id not in accessbot.get_grant_request_ids()
        assert "timed out" in mocked_testbot.pop_message()
        assert "not approved" in mocked_testbot.pop_message()
        assert self.raw_messages[0].to.person == self.sdm_admin
        assert self.raw_messages[1].to.person == self.sdm_admin

    def test_when_handling_messages_from_a_channel(self, mocked_testbot):
        accessbot = mocked_testbot.bot.plugin_manager.plugins['AccessBot']
        sender_id = accessbot.build_identifier(accessbot.config['SENDER_EMAIL_OVERRIDE'])
        sender_id.room = create_room_mock(self.channel_name)
        accessbot.enter_grant_request(access_request_id, Message(frm = sender_id), MagicMock(), MagicMock(), MagicMock())
        assert access_request_id in accessbot.get_grant_request_ids()

        PollerHelper(accessbot).stale_grant_requests_cleaner()

        assert access_request_id not in accessbot.get_grant_request_ids()
        assert "timed out" in mocked_testbot.pop_message()
        assert "not approved" in mocked_testbot.pop_message()
        assert self.raw_messages[0].to.person == self.sdm_admin
        assert self.raw_messages[1].to.person == f"#{self.channel_name}"


def create_room_mock(channel_name):
    mock = MagicMock()
    mock.name = channel_name
    return mock
