# pylint: disable=invalid-name
import pytest
import sys
from unittest.mock import MagicMock

from test_common import create_config, DummyResource
sys.path.append('plugins/sdm')

pytest_plugins = ["errbot.backends.test"]
extra_plugin_dir = 'plugins/sdm'

role_name = "Xxx"
access_request_id = "12ab"

class Test_assign_role:
    @pytest.fixture
    def mocked_testbot(self, testbot):
        config = create_config()
        return inject_mocks(testbot, config)

    @pytest.mark.skip
    def test_show_resources_command(self, mocked_testbot):
        mocked_testbot.push_message(f"assign role {role_name}")
        mocked_testbot.push_message(f"yes {access_request_id}")
        assert "valid request" in mocked_testbot.pop_message()
        assert "access request" in mocked_testbot.pop_message()
        assert "Granting" in mocked_testbot.pop_message()


# pylint: disable=dangerous-default-value
def inject_mocks(testbot, config):
    accessbot = testbot.bot.plugin_manager.plugins['AccessBot']
    accessbot.config = config
    accessbot.get_admins = MagicMock(return_value = ["gbin@localhost"])
    accessbot.get_api_access_key = MagicMock(return_value = "api-access_key")
    accessbot.get_api_secret_key = MagicMock(return_value = "c2VjcmV0LWtleQ==") # valid base64 string
    return testbot

