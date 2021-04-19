import pytest
import sys
from unittest.mock import MagicMock

sys.path.append('plugins/sdm')
from lib import AccessHelper
from properties import Properties

pytest_plugins = ["errbot.backends.test"]
extra_plugin_dir = 'plugins/sdm'

access_request_id = "12ab"

class Test_default_flow: # manual approval
    @pytest.fixture
    def mocked_testbot(self, testbot):
        props = create_properties()
        return inject_props(testbot, props)

    def test_access_command_grant_approved(self, mocked_testbot):
        mocked_testbot.push_message("access to Xxx")
        mocked_testbot.push_message(f"yes {access_request_id}")
        assert "valid request" in mocked_testbot.pop_message()
        assert "access request" in mocked_testbot.pop_message()
        assert "Granting" in mocked_testbot.pop_message()

    def test_access_command_grant_timed_out(self, mocked_testbot):
        mocked_testbot.push_message("access to Xxx")
        assert "valid request" in mocked_testbot.pop_message()
        assert "access request" in mocked_testbot.pop_message()
        assert "timed out" in mocked_testbot.pop_message()
        assert "not approved" in mocked_testbot.pop_message()

    def test_access_command_grant_not_approved(self, mocked_testbot):
        mocked_testbot.push_message("access to Xxx")
        mocked_testbot.push_message("no") # Anything but yes
        assert "valid request" in mocked_testbot.pop_message()
        assert "access request" in mocked_testbot.pop_message()
        assert "timed out" in mocked_testbot.pop_message()
        assert "not approved" in mocked_testbot.pop_message()

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


def inject_props(testbot, props):
    accessbot = testbot.bot.plugin_manager.plugins['AccessBot']
    mock_dict = {
        'get_access_helper': MagicMock(return_value = create_access_helper(accessbot, props)),
        'get_properties': MagicMock(return_value = props)
    }
    testbot.inject_mocks('AccessBot', mock_dict)
    return testbot

def create_access_helper(accessbot, props):
    helper = AccessHelper(
        props = props,
        admin_ids = accessbot.get_admin_ids(props.admins()),
        send_fn = accessbot.send,
        is_access_request_granted_fn = accessbot.is_access_request_granted,
        add_thumbsup_reaction_fn = accessbot.add_thumbsup_reaction,
        enter_access_request_fn = accessbot.enter_access_request,
        remove_access_request_fn = accessbot.remove_access_request    
    )
    helper.access_service = create_account_service_mock()
    helper.generate_access_request_id = MagicMock(return_value = access_request_id)
    return helper

def create_account_service_mock():
    service_mock = MagicMock()
    service_mock.get_resource_by_name = MagicMock(return_value = create_mock_resource())
    service_mock.get_account_by_email = MagicMock(return_value = create_mock_account())
    service_mock.grant_temporary_access = MagicMock()
    return service_mock

def create_mock_resource():
    mock_resource = MagicMock()
    mock_resource.id = 1
    mock_resource.name = "myresource"
    return mock_resource

def create_mock_account():
    mock_account = MagicMock()
    mock_account.id = 1
    mock_account.name = "myaccount@test.com"
    return mock_account

def create_properties():
    return Properties(
        admins = "gbin@localhost",
        admin_timeout = 1,
        api_access_key = "api-access_key",
        api_secret_key = "c2VjcmV0LWtleQ==",
        sender_nick_override = "testuser",
        sender_email_override = "testuser@localhost",
        auto_approve_all = False
    )
