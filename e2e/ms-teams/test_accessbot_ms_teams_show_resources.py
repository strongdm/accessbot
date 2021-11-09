import sys
import pytest
from unittest.mock import MagicMock

sys.path.append('plugins/sdm/')
sys.path.append('e2e/')

from test_common import DummyResource, create_config, callback_message_fn
from lib import ShowResourcesHelper

pytest_plugins = ["errbot.backends.test"]
extra_plugin_dir = "plugins/sdm"
account_name = "myaccount@test.com"

class Test_show_resources:
    extra_config = { 'BOT_PLATFORM': 'ms-teams' }

    @pytest.fixture
    def mocked_testbot(self, testbot):
        config = create_config()
        return inject_mocks(testbot, config)

    def test_fail_show_resources_command_when_sent_via_dm(self, mocked_testbot):
        mocked_testbot.push_message("show available resources")
        assert "cannot execute this command via DM" in mocked_testbot.pop_message()

    def test_show_resources_command_when_sent_via_team(self, mocked_testbot):
        mocked_testbot._bot.callback_message = MagicMock(side_effect=callback_message_fn(
            mocked_testbot._bot,
            from_email=account_name,
            approver_is_admin=True
        ))
        mocked_testbot.push_message("show available resources")
        message = mocked_testbot.pop_message()
        assert "Aaa (type: DummyResource)" in message
        assert "Bbb (type: DummyResource)" in message

def default_dummy_resources():
    return [ DummyResource("Bbb", {}), DummyResource("Aaa", {}) ]

def inject_mocks(testbot, config, resources = default_dummy_resources(), resources_by_role = []):
    accessbot = testbot.bot.plugin_manager.plugins['AccessBot']
    accessbot.config = config
    accessbot.get_admins = MagicMock(return_value = ["gbin@localhost"])
    accessbot.get_api_access_key = MagicMock(return_value = "api-access_key")
    accessbot.get_api_secret_key = MagicMock(return_value = "c2VjcmV0LWtleQ==") # valid base64 string
    accessbot.get_sdm_service = MagicMock(return_value = create_sdm_service_mock(resources, resources_by_role))
    accessbot.get_show_resources_helper = MagicMock(return_value = ShowResourcesHelper(accessbot))
    return testbot

def create_sdm_service_mock(resources, resources_by_role):
    service_mock = MagicMock()
    service_mock.get_all_resources = MagicMock(return_value = resources)
    service_mock.get_all_resources_by_role = MagicMock(return_value = resources_by_role)
    return service_mock
