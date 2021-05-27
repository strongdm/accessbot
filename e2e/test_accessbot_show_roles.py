# pylint: disable=invalid-name
import pytest
import sys
from unittest.mock import MagicMock

from test_common import create_config, DummyRole
sys.path.append('plugins/sdm')
from lib import ShowRolesHelper

pytest_plugins = ["errbot.backends.test"]
extra_plugin_dir = 'plugins/sdm'

class Test_show_roles:
    @pytest.fixture
    def mocked_testbot(self, testbot):
        config = create_config()
        return inject_mocks(testbot, config)

    def test_show_roles_command(self, mocked_testbot):
        mocked_testbot.push_message("show available roles")
        message = mocked_testbot.pop_message()
        assert "Aaa" in message
        assert "Bbb" in message


def default_dummy_roles():
    return [ DummyRole("Bbb"), DummyRole("Aaa") ]

# pylint: disable=dangerous-default-value
def inject_mocks(testbot, config, roles = default_dummy_roles()):
    accessbot = testbot.bot.plugin_manager.plugins['AccessBot']
    accessbot.config = config
    accessbot.get_admins = MagicMock(return_value = ["gbin@localhost"])
    accessbot.get_api_access_key = MagicMock(return_value = "api-access_key")
    accessbot.get_api_secret_key = MagicMock(return_value = "c2VjcmV0LWtleQ==") # valid base64 string
    accessbot.get_sdm_service = MagicMock(return_value = create_sdm_service_mock(roles))
    accessbot.get_show_roles_helper = MagicMock(return_value = ShowRolesHelper(accessbot))
    return testbot

def create_sdm_service_mock(roles):
    service_mock = MagicMock()
    service_mock.get_all_roles = MagicMock(return_value = roles)
    return service_mock
