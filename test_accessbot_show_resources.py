# pylint: disable=invalid-name
import pytest
import sys
from unittest.mock import MagicMock, patch

from test_accessbot_common import create_properties
sys.path.append('plugins/sdm')
from lib import ShowResourcesHelper

pytest_plugins = ["errbot.backends.test"]
extra_plugin_dir = 'plugins/sdm'

class Test_show_resources:
    @pytest.fixture
    def mocked_testbot(self, testbot):
        props = create_properties()
        return inject_mocks(testbot, props)

    def test_show_resources_command(self, mocked_testbot):
        mocked_testbot.push_message("show available resources")
        message = mocked_testbot.pop_message()
        assert "Aaa (type: DummyResource)" in message
        assert "Bbb (type: DummyResource)" in message

class Test_show_not_hidden_resources:
    @pytest.fixture
    def mocked_testbot(self, testbot):
        props = create_properties()
        props.hide_resource_tag = MagicMock(return_value = 'hidden-resource')
        resources = [ DummyResource("Bbb", {}), DummyResource("Aaa", {'hidden-resource': True}) ]
        return inject_mocks(testbot, props, resources)

    def test_show_resources_command(self, mocked_testbot):
        mocked_testbot.push_message("show available resources")
        message = mocked_testbot.pop_message()
        assert "Aaa (type: DummyResource)" not in message
        assert "Bbb (type: DummyResource)" in message


class DummyResource:
    def __init__(self, name, tags):
        self.name = name
        self.tags = tags

def default_dummy_resources():
    return [ DummyResource("Bbb", {}), DummyResource("Aaa", {}) ]

# pylint: disable=dangerous-default-value
def inject_mocks(testbot, props, resources = default_dummy_resources()):
    accessbot = testbot.bot.plugin_manager.plugins['AccessBot']
    mock_dict = {
        'get_show_resources_helper': MagicMock(return_value = create_show_resources_helper(accessbot, props, resources))
    }
    testbot.inject_mocks('AccessBot', mock_dict)
    return testbot

def create_show_resources_helper(accessbot, props, resources):
    with patch.object(accessbot, 'get_properties', return_value = props):
        helper = ShowResourcesHelper(accessbot)
        helper.access_service = create_access_service_mock(resources)
        return helper

def create_access_service_mock(resources):
    service_mock = MagicMock()
    service_mock.get_all_resources = MagicMock(return_value = resources)
    return service_mock
