# pylint: disable=invalid-name
import os
import pytest
import sys
from errbot.backends.base import Message
from unittest.mock import MagicMock

sys.path.append('e2e')
sys.path.append('plugins/sdm')

from test_common import create_config, send_message_override, ErrBotExtraTestSettings, get_dummy_person, DummyResource
from lib import PollerHelper

pytest_plugins = ["errbot.backends.test"]

access_request_id = "12ab"

class Test_stale_grant_requests_cleaner(ErrBotExtraTestSettings):
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

class Test_stale_max_auto_approve_cleaner(ErrBotExtraTestSettings):
    @pytest.fixture
    def mocked_testbot(self, testbot):
        config = create_config()
        accessbot = testbot.bot.plugin_manager.plugins['AccessBot']
        accessbot.config = config
        return testbot

    def test_when_theres_no_max_auto_approve_use_config(self, mocked_testbot):
        accessbot = mocked_testbot.bot.plugin_manager.plugins['AccessBot']
        accessbot.increase_auto_approve_uses_counter = MagicMock()
        PollerHelper(accessbot).stale_max_auto_approve_cleaner()
        accessbot.increase_auto_approve_uses_counter.assert_not_called()

    def test_when_auto_approve_uses_gets_cleaned(self, mocked_testbot):
        accessbot = mocked_testbot.bot.plugin_manager.plugins['AccessBot']
        accessbot.config['MAX_AUTO_APPROVE_INTERVAL'] = 1
        PollerHelper(accessbot).stale_max_auto_approve_cleaner()
        assert accessbot['auto_approve_uses'] == {}

class Test_stale_with_approvers_channel_tag_enabled(ErrBotExtraTestSettings):
    raw_messages = []
    regular_channel_name = 'regular-approvers-channel'
    approvers_channel_name = 'resource-approvers-channel'

    @pytest.fixture
    def mocked_testbot(self, testbot):
        self.raw_messages = []
        testbot.bot.send_message = send_message_override(testbot.bot, self.raw_messages)
        config = create_config()
        config['ADMIN_TIMEOUT'] = 0
        config['APPROVERS_CHANNEL_TAG'] = 'approvers-channel'
        accessbot = testbot.bot.plugin_manager.plugins['AccessBot']
        accessbot.config = config
        return testbot

    def test_send_stale_message_to_approvers_channel(self, mocked_testbot):
        accessbot = mocked_testbot.bot.plugin_manager.plugins['AccessBot']
        sender_id = accessbot.build_identifier(accessbot.config['SENDER_EMAIL_OVERRIDE'])
        sender_id.room = create_room_mock(self.regular_channel_name)
        accessbot.enter_grant_request(access_request_id, Message(frm=sender_id),
                                      DummyResource('resource', {'approvers-channel': self.approvers_channel_name}),
                                      MagicMock(), MagicMock())
        assert access_request_id in accessbot.get_grant_request_ids()
        assert "timed out" in mocked_testbot.pop_message()
        assert "not approved" in mocked_testbot.pop_message()
        assert self.raw_messages[0].to.person == f"#{self.approvers_channel_name}"
        assert self.raw_messages[1].to.person == f"#{self.regular_channel_name}"

def create_room_mock(channel_name):
    mock = MagicMock()
    mock.name = channel_name
    return mock
