# pylint: disable=invalid-name
import pytest
import sys
from unittest.mock import MagicMock

from test_common import create_config, DummyResource
sys.path.append('plugins/sdm')
from lib import ShowResourcesHelper

pytest_plugins = ["errbot.backends.test"]
extra_plugin_dir = 'plugins/sdm'

class Test_show_resources:
    @pytest.fixture
    def mocked_testbot(self, testbot):
        config = create_config()
        return inject_mocks(testbot, config)

    def test_show_resources_command(self, mocked_testbot):
        mocked_testbot.push_message("show available resources")
        message = mocked_testbot.pop_message()
        assert "Aaa (type: DummyResource)" in message
        assert "Bbb (type: DummyResource)" in message

class Test_show_allowed_resources:
    @pytest.fixture
    def mocked_testbot_allow_resource_true(self, testbot):
        config = create_config()
        config['ALLOW_RESOURCE_TAG'] = 'allow-resource'
        resources = [ DummyResource("Bbb", {}), DummyResource("Aaa", {'allow-resource': True}) ]
        return inject_mocks(testbot, config, resources)

    @pytest.fixture
    def mocked_testbot_allow_resource_false(self, testbot):
        config = create_config()
        config['ALLOW_RESOURCE_TAG'] = 'allow-resource'
        resources = [ DummyResource("Bbb", {}), DummyResource("Aaa", {'allow-resource': False}) ]
        return inject_mocks(testbot, config, resources)

    def test_only_show_allowed_resources_when_allow_resource_tag_true(self, mocked_testbot_allow_resource_true):
        mocked_testbot_allow_resource_true.push_message("show available resources")
        message = mocked_testbot_allow_resource_true.pop_message()
        assert "Aaa (type: DummyResource)" in message
        assert "Bbb (type: DummyResource)" not in message

    def test_dont_show_resources_when_allow_resource_tag_false(self, mocked_testbot_allow_resource_false):
        mocked_testbot_allow_resource_false.push_message("show available resources")
        message = mocked_testbot_allow_resource_false.pop_message()
        assert "Aaa (type: DummyResource)" not in message
        assert "Bbb (type: DummyResource)" not in message

class Test_not_show_hidden_resources:
    @pytest.fixture
    def mocked_testbot_hide_resource_true(self, testbot):
        config = create_config()
        config['HIDE_RESOURCE_TAG'] = 'hide-resource'
        resources = [ DummyResource("Bbb", {}), DummyResource("Aaa", {'hide-resource': True}) ]
        return inject_mocks(testbot, config, resources)

    @pytest.fixture
    def mocked_testbot_hide_resource_false(self, testbot):
        config = create_config()
        config['HIDE_RESOURCE_TAG'] = 'hide-resource'
        resources = [ DummyResource("Bbb", {}), DummyResource("Aaa", {'hide-resource': False}) ]
        return inject_mocks(testbot, config, resources)

    def test_show_resources_when_hide_resource_tag_true(self, mocked_testbot_hide_resource_true):
        mocked_testbot_hide_resource_true.push_message("show available resources")
        message = mocked_testbot_hide_resource_true.pop_message()
        assert "Aaa (type: DummyResource)" not in message
        assert "Bbb (type: DummyResource)" in message

    def test_show_resources_when_hide_resource_tag_false(self, mocked_testbot_hide_resource_false):
        mocked_testbot_hide_resource_false.push_message("show available resources")
        message = mocked_testbot_hide_resource_false.pop_message()
        assert "Aaa (type: DummyResource)" in message
        assert "Bbb (type: DummyResource)" in message

class Test_show_resources_by_role:
    @pytest.fixture
    def mocked_testbot(self, testbot):
        config = create_config()
        config['CONTROL_RESOURCES_ROLE_NAME'] = 'myrole'
        resources_by_role = [ DummyResource("Bbb in role", {}), DummyResource("Aaa in role", {}) ]
        return inject_mocks(testbot, config, resources_by_role = resources_by_role)

    def test_show_resources_command(self, mocked_testbot):
        mocked_testbot.push_message("show available resources")
        message = mocked_testbot.pop_message()
        assert "Aaa in role (type: DummyResource)" in message
        assert "Bbb in role (type: DummyResource)" in message


def default_dummy_resources():
    return [ DummyResource("Bbb", {}), DummyResource("Aaa", {}) ]

# pylint: disable=dangerous-default-value
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
