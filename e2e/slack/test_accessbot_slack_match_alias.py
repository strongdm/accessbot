# pylint: disable=invalid-name
import sys
import pytest
from unittest.mock import MagicMock

sys.path.append('plugins/sdm')
sys.path.append('e2e/')

from test_common import create_config, DummyResource, get_dummy_person
from lib import ShowResourcesHelper

pytest_plugins = ["errbot.backends.test"]
extra_plugin_dir = 'plugins/sdm'

show_resources_command = 'show available resources'
show_resources_alias = 'sares'
access_to_resource_command = 'access to'
access_to_resource_alias = 'acres'
resource_id = 1
resource_name = "myresource"
account_id = 1
account_name = "myaccount@test.com"
access_request_id = "12ab"


class Test_match_alias:
    extra_config = {
        'BOT_COMMANDS_ALIASES': {
            'show_resources': show_resources_alias,
            'access_resource': access_to_resource_alias
        }
    }

    @pytest.fixture
    def mocked_testbot(self, testbot):
        config = create_config()
        testbot.bot.plugin_manager.plugins['AccessBot'].get_admin_ids = MagicMock(
            return_value = [get_dummy_person(account_name, is_deleted=False)]
        )
        return inject_config(testbot, config)

    @pytest.fixture
    def mocked_sdm_service(self, mocked_testbot):
        accessbot = mocked_testbot.bot.plugin_manager.plugins['AccessBot']
        return accessbot.get_sdm_service.return_value

    def test_full_command_without_argument(self, mocked_testbot, mocked_sdm_service):
        mocked_testbot.push_message(show_resources_command)
        message = mocked_testbot.pop_message()
        assert "Aaa (type: DummyResource)" in message
        assert "Bbb (type: DummyResource)" in message

    def test_command_alias_without_argument(self, mocked_testbot, mocked_sdm_service):
        mocked_testbot.push_message(show_resources_alias)
        message = mocked_testbot.pop_message()
        assert "Aaa (type: DummyResource)" in message
        assert "Bbb (type: DummyResource)" in message

    def test_full_command_with_argument(self, mocked_testbot, mocked_sdm_service):
        mocked_testbot.push_message(access_to_resource_command + f' {resource_name}')
        assert "valid request" in mocked_testbot.pop_message()
        assert "access request" in mocked_testbot.pop_message()

    def test_command_alias_with_argument(self, mocked_testbot, mocked_sdm_service):
        mocked_testbot.push_message(access_to_resource_alias + f' {resource_name}')
        assert "valid request" in mocked_testbot.pop_message()
        assert "access request" in mocked_testbot.pop_message()


# pylint: disable=dangerous-default-value
def inject_config(testbot, config):
    accessbot = testbot.bot.plugin_manager.plugins['AccessBot']
    accessbot.config = config
    # The default implementation is not compatible with the backend identifier.
    # Refer to: https://errbot.readthedocs.io/en/4.1/errbot.backends.test.html#errbot.backends.test.TestPerson
    accessbot.get_admins = MagicMock(return_value = ["gbin@localhost"])
    accessbot.get_api_access_key = MagicMock(return_value = "api-access_key")
    accessbot.get_api_secret_key = MagicMock(return_value = "c2VjcmV0LWtleQ==")  # valid base64 string
    accessbot.get_sdm_service = MagicMock(return_value = create_sdm_service_mock())
    accessbot.get_show_resources_helper = MagicMock(return_value = ShowResourcesHelper(accessbot))
    return testbot

def create_sdm_service_mock():
    mock = MagicMock()
    mock.get_account_by_email = MagicMock(return_value = create_account_mock(account_tags={}))
    mock.account_grant_exists = MagicMock(return_value = False)
    mock.get_all_resources = MagicMock(return_value = [DummyResource("Aaa", {}), DummyResource("Bbb", {})])
    return mock

def create_resource_mock(tags):
    mock = MagicMock()
    mock.id = resource_id
    mock.name = resource_name
    mock.tags = tags
    return mock

def create_account_mock(account_email = account_name, account_tags={}):
    mock = MagicMock()
    mock.id = account_id
    mock.name = account_name
    mock.email = account_email
    mock.tags = account_tags
    return mock
