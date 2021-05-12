# pylint: disable=invalid-name
import datetime
import sys
from unittest.mock import MagicMock, Mock, patch
import pytest

from test_common import create_config
sys.path.append('plugins/sdm')
from lib import AccessHelper, ApproveHelper, PollerHelper

pytest_plugins = ["errbot.backends.test"]
extra_plugin_dir = 'plugins/sdm'

resource_id = 1
resource_name = "myresource"
account_id = 1
account_name = "myaccount@test.com"
access_request_id = "12ab"

class Test_default_flow: # manual approval
    @pytest.fixture
    def mocked_testbot(self, testbot):
        config = create_config()
        return inject_config(testbot, config)

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

    def test_access_command_grant_bolded_yes_message(self, mocked_testbot):
        mocked_testbot.push_message("access to Xxx")
        mocked_testbot.push_message(f"**yes {access_request_id}**")
        assert "valid request" in mocked_testbot.pop_message()
        assert "access request" in mocked_testbot.pop_message()
        assert "Granting" in mocked_testbot.pop_message()

    def test_access_command_grant_bolded_request_id_in_yes_message(self, mocked_testbot):
        mocked_testbot.push_message("access to Xxx")
        mocked_testbot.push_message(f"yes *{access_request_id}*")
        assert "valid request" in mocked_testbot.pop_message()
        assert "access request" in mocked_testbot.pop_message()
        assert "Granting" in mocked_testbot.pop_message()

    def test_access_command_grant_bolded_access_message(self, mocked_testbot):
        mocked_testbot.push_message("**access to Xxx**")
        mocked_testbot.push_message(f"yes {access_request_id}")
        assert "valid request" in mocked_testbot.pop_message()
        assert "access request" in mocked_testbot.pop_message()
        assert "Granting" in mocked_testbot.pop_message()

class Test_automatic_approval_flow:
    @pytest.fixture
    def mocked_testbot(self, testbot):
        config = create_config()
        config['AUTO_APPROVE_ALL'] = True
        return inject_config(testbot, config)

    def test_access_command_grant_auto_approved_for_all(self, mocked_testbot):
        mocked_testbot.push_message("access to Xxx")
        assert "Granting" in mocked_testbot.pop_message()


class Test_multiple_admins_flow:
    @pytest.fixture
    def mocked_testbot(self, testbot):
        config = create_config()
        return inject_config(testbot, config, admins = ["gbin@localhost",  "user1"])

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
        config = create_config()
        config['AUTO_APPROVE_TAG'] = "auto-approve"
        return inject_config(testbot, config, tags = {'auto-approve': True})

    def test_access_command_grant_auto_approved_for_tagged_resource(self, mocked_testbot):
        mocked_testbot.push_message("access to Xxx")
        assert "Granting" in mocked_testbot.pop_message()

class Test_hide_resource_tag:
    @pytest.fixture
    def mocked_testbot(self, testbot):
        config = create_config()
        config['HIDE_RESOURCE_TAG'] = "hide-resource"
        return inject_config(testbot, config, tags = {'hide-resource': True})

    def test_access_command_grant_auto_approved_for_tagged_resource(self, mocked_testbot):
        mocked_testbot.push_message("access to Xxx")
        assert "Invalid" in mocked_testbot.pop_message()

class Test_grant_timeout:
    @pytest.fixture
    def mocked_testbot(self, testbot):
        config = create_config()
        config['GRANT_TIMEOUT'] = 1
        return inject_config(testbot, config)

    class NewDate(datetime.datetime):
        @classmethod
        def now(cls, tz=None):
            return cls(2021, 5, 12)

    def test_access_command_grant_with_custom_timeout(self, mocked_testbot):
        accessbot = mocked_testbot.bot.plugin_manager.plugins['AccessBot']
        grant_temporary_access_mock = accessbot.get_access_service().grant_temporary_access
        with patch('datetime.datetime', new = self.NewDate):
            mocked_testbot.push_message("access to Xxx")
            mocked_testbot.push_message(f"yes {access_request_id}")
            assert "valid request" in mocked_testbot.pop_message()
            assert "access request" in mocked_testbot.pop_message()
            assert "Granting" in mocked_testbot.pop_message()

            start_from = datetime.datetime(2021, 5, 12, 0, 0)
            valid_until = datetime.datetime(2021, 5, 12, 0, 1)
            grant_temporary_access_mock.assert_called_with(resource_id, account_id, start_from, valid_until)


# pylint: disable=dangerous-default-value
def inject_config(testbot, config, admins = ["gbin@localhost"], tags = {}):
    accessbot = testbot.bot.plugin_manager.plugins['AccessBot']
    accessbot.config = config
    accessbot.start_poller(0.5, PollerHelper(accessbot).stale_access_requests_cleaner)
    accessbot.get_admins = MagicMock(return_value = admins)
    accessbot.get_api_access_key = MagicMock(return_value = "api-access_key")
    accessbot.get_api_secret_key = MagicMock(return_value = "c2VjcmV0LWtleQ==") # valid base64 string
    accessbot.get_access_service = MagicMock(return_value = create_access_service_mock(tags))
    accessbot.get_access_helper = MagicMock(return_value = create_access_helper(accessbot))
    accessbot.get_approve_helper = MagicMock(return_value = create_approve_helper(accessbot))
    return testbot

def create_access_helper(accessbot):
    helper = AccessHelper(accessbot)
    helper.generate_access_request_id = MagicMock(return_value = access_request_id)
    return helper

def create_approve_helper(accessbot):
    return ApproveHelper(accessbot)

def create_access_service_mock(tags):
    service_mock = MagicMock()
    service_mock.get_resource_by_name = MagicMock(return_value = create_mock_resource(tags))
    service_mock.get_account_by_email = MagicMock(return_value = create_mock_account())
    service_mock.grant_temporary_access = MagicMock()
    return service_mock

def create_mock_resource(tags):
    mock_resource = MagicMock()
    mock_resource.id = resource_id
    mock_resource.name = resource_name
    mock_resource.tags = tags
    return mock_resource

def create_mock_account():
    mock_account = MagicMock()
    mock_account.id = account_id
    mock_account.name = account_name
    return mock_account
