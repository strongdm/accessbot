import pytest
import sys
from unittest.mock import MagicMock

sys.path.append('plugins/sdm')
from lib import ShowResourcesHelper
import properties

pytest_plugins = ["errbot.backends.test"]
extra_plugin_dir = 'plugins/sdm'

class Test_show_resources: 
    @pytest.fixture
    def mocked_testbot(self, testbot):
        props = properties.get()
        mock_dict = {
            'get_show_resources_helper': MagicMock(return_value = create_show_resources_helper(props)),
            'get_properties': MagicMock(return_value = props)
        }
        testbot.inject_mocks('AccessBot', mock_dict)
        return testbot

    def test_show_resources_command(self, mocked_testbot):
        mocked_testbot.push_message("show available resources")
        message = mocked_testbot.pop_message()
        assert "Aaa (type: DummyResource)" in message
        assert "Bbb (type: DummyResource)" in message


def create_show_resources_helper(props):
    helper = ShowResourcesHelper(props)
    helper.access_service = create_access_service_mock()
    return helper

def create_access_service_mock():
    service_mock = MagicMock()
    service_mock.get_all_resources = MagicMock(return_value = [
        DummyResource("Bbb"),
        DummyResource("Aaa")
    ])
    return service_mock

class DummyResource:
    def __init__(self, name):
        self.name = name
        self.tags = {}
