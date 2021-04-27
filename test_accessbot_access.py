# pylint: disable=invalid-name
import pytest
import sys
from unittest.mock import MagicMock, patch

from test_accessbot_common import create_properties
sys.path.append('plugins/sdm')
from lib import AccessHelper

pytest_plugins = ["errbot.backends.test"]
extra_plugin_dir = 'plugins/sdm'

access_request_id = "12ab"

class Test_default_flow: # manual approval
    @pytest.fixture
    def mocked_testbot(self, testbot):
        props = create_properties()
        return inject_props(testbot, props)

    @pytest.fixture
    def mocked_testbot_short_timeout(self, testbot):
        props = create_properties()
        props.admin_timeout = MagicMock(return_value = 1)
        return inject_props(testbot, props)

    def test_access_command_grant_approved(self, mocked_testbot):
        mocked_testbot.push_message("access to Xxx")
        mocked_testbot.push_message(f"yes {access_request_id}")
        assert "valid request" in mocked_testbot.pop_message()
        assert "access request" in mocked_testbot.pop_message()
        assert "Granting" in mocked_testbot.pop_message()

    def test_access_command_grant_timed_out(self, mocked_testbot_short_timeout):
        mocked_testbot_short_timeout.push_message("access to Xxx")
        assert "valid request" in mocked_testbot_short_timeout.pop_message()
        assert "access request" in mocked_testbot_short_timeout.pop_message()
        assert "timed out" in mocked_testbot_short_timeout.pop_message()
        assert "not approved" in mocked_testbot_short_timeout.pop_message()

    def test_access_command_grant_not_approved(self, mocked_testbot_short_timeout):
        mocked_testbot_short_timeout.push_message("access to Xxx")
        mocked_testbot_short_timeout.push_message("no") # Anything but yes
        assert "valid request" in mocked_testbot_short_timeout.pop_message()
        assert "access request" in mocked_testbot_short_timeout.pop_message()
        assert "timed out" in mocked_testbot_short_timeout.pop_message()
        assert "not approved" in mocked_testbot_short_timeout.pop_message()

    def test_access_command_grant_approved_bolded_yes_message(self, mocked_testbot):
        mocked_testbot.push_message("access to Xxx")
        mocked_testbot.push_message(f"**yes {access_request_id}**")
        assert "valid request" in mocked_testbot.pop_message()
        assert "access request" in mocked_testbot.pop_message()
        assert "Granting" in mocked_testbot.pop_message()

    def test_access_command_grant_approved_italicized_yes_message(self, mocked_testbot):
        mocked_testbot.push_message("access to Xxx")
        mocked_testbot.push_message(f"_yes {access_request_id}_")
        assert "valid request" in mocked_testbot.pop_message()
        assert "access request" in mocked_testbot.pop_message()
        assert "Granting" in mocked_testbot.pop_message()

class Test_automatic_approval_flow:
    @pytest.fixture
    def mocked_testbot(self, testbot):
        props = create_properties()
        props.auto_approve_all = MagicMock(return_value = True)
        return inject_props(testbot, props)

    def test_access_command_grant_auto_approved_for_all(self, mocked_testbot):
        mocked_testbot.push_message("access to Xxx")
        assert "Granting" in mocked_testbot.pop_message()

class Test_multiple_admins_flow:
    @pytest.fixture
    def mocked_testbot(self, testbot):
        props = create_properties()
        props.admins = MagicMock(return_value = ["gbin@localhost",  "user1"])
        return inject_props(testbot, props)

    def test_access_command_grant_multiple_admins(self, mocked_testbot):
        mocked_testbot.push_message("access to Xxx")
        mocked_testbot.push_message(f"yes {access_request_id}")
        assert "valid request" in mocked_testbot.pop_message()
        assert "access request" in mocked_testbot.pop_message()
        assert "access request" in mocked_testbot.pop_message()
        assert "Granting" in mocked_testbot.pop_message()

class Test_auto_approve_tag:
    @pytest.fixture
    def mocked_testbot(self, testbot):
        props = create_properties()
        props.auto_approve_tag = MagicMock(return_value = "auto-approve")
        return inject_props(testbot, props, tags = {'auto-approve': True})

    def test_access_command_grant_auto_approved_for_tagged_resource(self, mocked_testbot):
        mocked_testbot.push_message("access to Xxx")
        assert "Granting" in mocked_testbot.pop_message()

class Test_hide_resource_tag:
    @pytest.fixture
    def mocked_testbot(self, testbot):
        props = create_properties()
        props.hide_resource_tag = MagicMock(return_value = "hide-resource")
        return inject_props(testbot, props, tags = {'hide-resource': True})

    def test_access_command_grant_auto_approved_for_tagged_resource(self, mocked_testbot):
        mocked_testbot.push_message("access to Xxx")
        assert "Invalid" in mocked_testbot.pop_message()


# pylint: disable=dangerous-default-value
def inject_props(testbot, props, tags = {}):
    accessbot = testbot.bot.plugin_manager.plugins['AccessBot']
    mock_dict = {
        'get_access_helper': MagicMock(return_value = create_access_helper(accessbot, props, tags))
    }
    testbot.inject_mocks('AccessBot', mock_dict)
    return testbot

def create_access_helper(accessbot, props, tags):
    with patch.object(accessbot, 'get_properties', return_value = props):
        helper = AccessHelper(accessbot)
        helper.access_service = create_access_service_mock(tags)
        helper.generate_access_request_id = MagicMock(return_value = access_request_id)
        return helper

def create_access_service_mock(tags):
    service_mock = MagicMock()
    service_mock.get_resource_by_name = MagicMock(return_value = create_mock_resource(tags))
    service_mock.get_account_by_email = MagicMock(return_value = create_mock_account())
    service_mock.grant_temporary_access = MagicMock()
    return service_mock

def create_mock_resource(tags):
    mock_resource = MagicMock()
    mock_resource.id = 1
    mock_resource.name = "myresource"
    mock_resource.tags = tags
    return mock_resource

def create_mock_account():
    mock_account = MagicMock()
    mock_account.id = 1
    mock_account.name = "myaccount@test.com"
    return mock_account
