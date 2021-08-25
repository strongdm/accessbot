# pylint: disable=invalid-name
import datetime
import pytest
import sys
import time
from unittest.mock import MagicMock, patch

from test_common import create_config, DummyRole

sys.path.append('plugins/sdm')
from lib import ApproveHelper, RoleGrantHelper, PollerHelper
from lib.exceptions import NotFoundException

pytest_plugins = ["errbot.backends.test"]
extra_plugin_dir = 'plugins/sdm'

role_id = 111
role_name = "role-name"
resource_id = 1
resource_name = "myresource"
account_id = 1
account_name = "myaccount@test.com"
access_request_id = "12ab"

class Test_assign_role:
    @pytest.fixture
    def mocked_testbot(self, testbot):
        config = create_config()
        return inject_mocks(testbot, config)

    class NewDate(datetime.datetime):
        @classmethod
        def now(cls, tz=None):
            return cls(2021, 5, 12)

    def test_assign_role_command(self, mocked_testbot):
        accessbot = mocked_testbot.bot.plugin_manager.plugins['AccessBot']
        grant_temporary_access_mock = accessbot.get_sdm_service().grant_temporary_access
        with patch('datetime.datetime', new = self.NewDate):
            push_access_role_request(mocked_testbot)
            mocked_testbot.push_message(f"yes {access_request_id}")
            assert "valid request" in mocked_testbot.pop_message()
            assert "assign request" in mocked_testbot.pop_message()
            assert "Granting" in mocked_testbot.pop_message()

            start_from = datetime.datetime(2021, 5, 12, 0, 0)
            valid_until = datetime.datetime(2021, 5, 12, 1, 0)
            grant_temporary_access_mock.assert_called_with(resource_id, account_id, start_from, valid_until)

class Test_auto_approve_all:
    @pytest.fixture
    def mocked_testbot(self, testbot):
        config = create_config()
        config['AUTO_APPROVE_ROLE_ALL'] = True
        return inject_mocks(testbot, config)

    @pytest.fixture
    def mocked_with_max_auto_approve(self, mocked_testbot):
        accessbot = mocked_testbot.bot.plugin_manager.plugins['AccessBot']
        accessbot.config['MAX_AUTO_APPROVE_USES'] = 1
        accessbot.config['MAX_AUTO_APPROVE_INTERVAL'] = 1
        return mocked_testbot

    def test_auto_all(self, mocked_testbot):
        push_access_role_request(mocked_testbot)
        assert "Granting" in mocked_testbot.pop_message()

    def test_with_remaining_approvals_message(self, mocked_with_max_auto_approve):
        push_access_role_request(mocked_with_max_auto_approve)
        assert "Granting" in mocked_with_max_auto_approve.pop_message()
        assert "remaining" in mocked_with_max_auto_approve.pop_message()

    def test_default_flow_once_exhausted_auto_approvals(self, mocked_with_max_auto_approve):
        push_access_role_request(mocked_with_max_auto_approve)
        assert "Granting" in mocked_with_max_auto_approve.pop_message()
        assert "remaining" in mocked_with_max_auto_approve.pop_message()
        push_access_role_request(mocked_with_max_auto_approve)
        mocked_with_max_auto_approve.push_message(f"yes {access_request_id}")
        assert "valid request" in mocked_with_max_auto_approve.pop_message()
        assert "assign request" in mocked_with_max_auto_approve.pop_message()
        assert "Granting" in mocked_with_max_auto_approve.pop_message()

    def test_keep_remaining_approvals_when_cleaner_passes(self, mocked_with_max_auto_approve):
        push_access_role_request(mocked_with_max_auto_approve)
        assert "Granting" in mocked_with_max_auto_approve.pop_message()
        assert "remaining" in mocked_with_max_auto_approve.pop_message()
        accessbot = mocked_with_max_auto_approve.bot.plugin_manager.plugins['AccessBot']
        PollerHelper(accessbot).stale_max_auto_approve_cleaner()
        push_access_role_request(mocked_with_max_auto_approve)
        assert "Granting" in mocked_with_max_auto_approve.pop_message()
        assert "remaining" in mocked_with_max_auto_approve.pop_message()

class Test_auto_approve_tag:
    @pytest.fixture
    def mocked_testbot(self, testbot):
        config = create_config()
        config['AUTO_APPROVE_ROLE_TAG'] = "sdm-roles"
        return inject_mocks(testbot, config, account_tags = {'sdm-roles': ''})

    def test_access_command_grant_auto_approved_for_tagged_resource(self, mocked_testbot):
        push_access_role_request(mocked_testbot)
        assert "Granting" in mocked_testbot.pop_message()

class Test_role_fuzzy_matching:
    role = "Very Long Role"

    @pytest.fixture
    def mocked_testbot(self, testbot):
        config = create_config()
        roles = [ DummyRole(self.role) ]
        return inject_mocks(testbot, config, roles, throw_no_role_found = True)

    def test_find_role_fuzzy_matching(self, mocked_testbot):
        mocked_testbot.push_message("access to role Long name")
        time.sleep(0.2)
        assert "cannot find that role" in mocked_testbot.pop_message()
        recommendation = mocked_testbot.pop_message()
        assert "Did you mean" in recommendation
        assert self.role in recommendation

    def test_fail_role_find_fuzzy_matching(self, mocked_testbot):
        mocked_testbot.push_message("access to role name") # it's too short, the threshold is not good enough
        time.sleep(0.2)
        assert "cannot find that role" in mocked_testbot.pop_message()

class Test_control_role_by_tag:
    no_allowed_role = "Very Long Role"
    allowed_role = "Second Role"
    roles = [DummyRole("Very Long Role"), DummyRole("Second Role")]
    tag_role_list = ["Second Role"]

    @pytest.fixture
    def mocked_testbot(self, testbot):
        config = create_config()
        config['USER_ROLES_TAG'] = 'sdm-roles'
        account_tags = { config['USER_ROLES_TAG']: ','.join(self.tag_role_list) }
        return inject_mocks(testbot, config, self.roles, account_tags, False)

    def test_success_get_access(self, mocked_testbot):
        mocked_testbot.push_message(f"access to role {self.allowed_role}")
        mocked_testbot.push_message(f"yes {access_request_id}")
        time.sleep(0.2)
        assert "valid request" in mocked_testbot.pop_message()
        assert "assign request" in mocked_testbot.pop_message()
        assert "Granting" in mocked_testbot.pop_message()

    def test_fail_get_access(self, mocked_testbot):
        mocked_testbot.push_message(f"access to role {self.no_allowed_role}")
        time.sleep(0.2)
        assert "not allowed" in mocked_testbot.pop_message()

 # pylint: disable=dangerous-default-value
def inject_mocks(testbot, config, roles = [], account_tags = None, throw_no_role_found = False):
    accessbot = testbot.bot.plugin_manager.plugins['AccessBot']
    accessbot.config = config
    accessbot.get_admins = MagicMock(return_value = ["gbin@localhost"])
    accessbot.get_api_access_key = MagicMock(return_value = "api-access_key")
    accessbot.get_api_secret_key = MagicMock(return_value = "c2VjcmV0LWtleQ==") # valid base64 string
    accessbot.get_sdm_service = MagicMock(return_value = create_sdm_service_mock(roles, account_tags, throw_no_role_found))
    accessbot.get_role_grant_helper = MagicMock(return_value = create_role_grant_helper(accessbot))
    accessbot.get_approve_helper = MagicMock(return_value = create_approve_helper(accessbot))
    return testbot

def create_role_grant_helper(accessbot):
    helper = RoleGrantHelper(accessbot)
    helper.generate_grant_request_id = MagicMock(return_value = access_request_id)
    return helper

def create_approve_helper(accessbot):
    return ApproveHelper(accessbot)

def create_sdm_service_mock(roles, account_tags, throw_no_role_found):
    service_mock = MagicMock()
    if throw_no_role_found:
        service_mock.get_role_by_name = MagicMock(side_effect = raise_no_role_found)
    else:
        service_mock.get_role_by_name = MagicMock(return_value = create_mock_role())
    service_mock.get_account_by_email = MagicMock(return_value = create_mock_account(account_tags))
    service_mock.get_all_resources_by_role = MagicMock(return_value = create_mock_resources())
    service_mock.grant_exists = MagicMock(return_value = False)
    service_mock.get_all_roles = MagicMock(return_value = roles)
    return service_mock

def create_mock_account(account_tags):
    mock_account = MagicMock()
    mock_account.id = account_id
    mock_account.name = account_name
    mock_account.tags = account_tags
    return mock_account

def create_mock_role():
    mock_role = MagicMock()
    mock_role.id = role_id
    mock_role.name = role_name
    return mock_role

def create_mock_resources():
    mock_resource = MagicMock()
    mock_resource.id = resource_id
    mock_resource.name = resource_name
    return [mock_resource]

def push_access_role_request(testbot):
    testbot.push_message(f"access to role {role_name}")
    # gives some time to process
    # needed in slow environments, e.g. github actions
    time.sleep(0.2)

def raise_no_role_found(message = '', match = ''):
    raise NotFoundException('Sorry, cannot find that role!')
