# pylint: disable=invalid-name
import sys
import time
import datetime
import pytest
from unittest.mock import MagicMock, patch

sys.path.append('plugins/sdm')
sys.path.append('e2e')

from test_common import create_config, DummyRole, get_dummy_person, ErrBotExtraTestSettings
from lib import ApproveHelper, RoleGrantHelper, PollerHelper
from lib.exceptions import NotFoundException

pytest_plugins = ["errbot.backends.test"]

role_id = 111
role_name = "role-name"
resource_id = 1
resource_name = "myresource"
account_id = 1
account_name = "myaccount@test.com"
access_request_id = "12AB"

class Test_assign_role(ErrBotExtraTestSettings):
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
            mocked_testbot.push_message(f"access to role {role_name}")
            mocked_testbot.push_message(f"yes {access_request_id}")
            assert "valid request" in mocked_testbot.pop_message()
            assert "assign request" in mocked_testbot.pop_message()
            assert "Granting" in mocked_testbot.pop_message()

            start_from = datetime.datetime(2021, 5, 12, 0, 0)
            valid_until = datetime.datetime(2021, 5, 12, 1, 0)
            grant_temporary_access_mock.assert_called_with(resource_id, account_id, start_from, valid_until)

    def test_assign_role_command_with_strange_casing(self, mocked_testbot):
        mocked_testbot.push_message(f"ACceSS To rOLe {role_name}")
        mocked_testbot.push_message(f"YeS {access_request_id}")
        assert "valid request" in mocked_testbot.pop_message()
        assert "assign request" in mocked_testbot.pop_message()
        assert "Granting" in mocked_testbot.pop_message()

class Test_auto_approve_all(ErrBotExtraTestSettings):
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
        mocked_testbot.push_message(f"access to role {role_name}")
        assert "Granting" in mocked_testbot.pop_message()

    def test_with_remaining_approvals_message(self, mocked_with_max_auto_approve):
        mocked_with_max_auto_approve.push_message(f"access to role {role_name}")
        assert "Granting" in mocked_with_max_auto_approve.pop_message()
        assert "remaining" in mocked_with_max_auto_approve.pop_message()

    def test_default_flow_once_exhausted_auto_approvals(self, mocked_with_max_auto_approve):
        mocked_with_max_auto_approve.push_message(f"access to role {role_name}")
        assert "Granting" in mocked_with_max_auto_approve.pop_message()
        assert "remaining" in mocked_with_max_auto_approve.pop_message()
        mocked_with_max_auto_approve.push_message(f"access to role {role_name}")
        mocked_with_max_auto_approve.push_message(f"yes {access_request_id}")
        assert f'Request auto-approved' in mocked_with_max_auto_approve.pop_message()
        assert "valid request" in mocked_with_max_auto_approve.pop_message()
        assert "assign request" in mocked_with_max_auto_approve.pop_message()
        assert "Granting" in mocked_with_max_auto_approve.pop_message()

    def test_keep_remaining_approvals_when_cleaner_passes(self, mocked_with_max_auto_approve):
        mocked_with_max_auto_approve.push_message(f"access to role {role_name}")
        assert "Granting" in mocked_with_max_auto_approve.pop_message()
        assert "remaining" in mocked_with_max_auto_approve.pop_message()
        accessbot = mocked_with_max_auto_approve.bot.plugin_manager.plugins['AccessBot']
        PollerHelper(accessbot).stale_max_auto_approve_cleaner()
        mocked_with_max_auto_approve.push_message(f"access to role {role_name}")
        assert f'Request auto-approved' in mocked_with_max_auto_approve.pop_message()
        assert "Granting" in mocked_with_max_auto_approve.pop_message()
        assert "remaining" in mocked_with_max_auto_approve.pop_message()

class Test_auto_approve_tag(ErrBotExtraTestSettings):
    @pytest.fixture
    def mocked_testbot(self, testbot):
        config = create_config()
        config['AUTO_APPROVE_ROLE_TAG'] = "auto-approve-role"
        return inject_mocks(testbot, config, role_tags = {'auto-approve-role': ''})

    def test_access_command_grant_auto_approved_for_tagged_resource(self, mocked_testbot):
        mocked_testbot.push_message(f"access to role {role_name}")
        assert "Granting" in mocked_testbot.pop_message()

class Test_role_fuzzy_matching(ErrBotExtraTestSettings):
    role = "Very Long Role"

    @pytest.fixture
    def mocked_testbot(self, testbot):
        config = create_config()
        roles = [ DummyRole(self.role, {}) ]
        return inject_mocks(testbot, config, roles, throw_no_role_found = True)

    def test_find_role_fuzzy_matching(self, mocked_testbot):
        mocked_testbot.push_message("access to role Long name")
        assert "cannot find that role" in mocked_testbot.pop_message()
        recommendation = mocked_testbot.pop_message()
        assert "Did you mean" in recommendation
        assert self.role in recommendation

    def test_fail_role_find_fuzzy_matching(self, mocked_testbot):
        mocked_testbot.push_message("access to role name") # it's too short, the threshold is not good enough
        assert "cannot find that role" in mocked_testbot.pop_message()

class Test_control_role_by_tag(ErrBotExtraTestSettings):
    no_allowed_role = "Very Long Role"
    allowed_role = "Second Role"
    roles = [DummyRole("Very Long Role", {}), DummyRole("Second Role", {})]
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
        assert "valid request" in mocked_testbot.pop_message()
        assert "assign request" in mocked_testbot.pop_message()
        assert "Granting" in mocked_testbot.pop_message()

    def test_fail_get_access(self, mocked_testbot):
        mocked_testbot.push_message(f"access to role {self.no_allowed_role}")
        assert "not allowed" in mocked_testbot.pop_message()

class Test_control_role_by_tag_without_roles(ErrBotExtraTestSettings):
    no_allowed_role = "Very Long Role"
    allowed_role = "Second Role"
    roles = [DummyRole("Very Long Role", {}), DummyRole("Second Role", {})]
    tag_role_list = ["Second Role"]

    @pytest.fixture
    def mocked_testbot(self, testbot):
        config = create_config()
        config['USER_ROLES_TAG'] = 'sdm-roles'
        account_tags = { config['USER_ROLES_TAG']: '' }
        return inject_mocks(testbot, config, self.roles, account_tags, False)

    def test_with_sdm_roles_empty(self, mocked_testbot):
        mocked_testbot.push_message(f"access to role {self.allowed_role}")
        assert "not allowed" in mocked_testbot.pop_message()

class Test_role_grant_exists(ErrBotExtraTestSettings):
    @pytest.fixture
    def mocked_testbot(self, testbot):
        config = create_config()
        return inject_mocks(testbot, config, role_grant_exists = True)

    def test_when_grant_exists(self, mocked_testbot):
        mocked_testbot.push_message("access to role Granted Role")
        mocked_testbot.push_message(f"yes {access_request_id}")
        assert "valid request" in mocked_testbot.pop_message()
        assert "assign request" in mocked_testbot.pop_message()
        assert "already have access" in mocked_testbot.pop_message()

    def test_when_grant_doesnt_exists(self, mocked_testbot):
        accessbot = mocked_testbot.bot.plugin_manager.plugins['AccessBot']
        service = accessbot.get_sdm_service()
        service.get_granted_resources_via_role.return_value = []
        mocked_testbot.push_message("access to role Allowed Role")
        mocked_testbot.push_message(f"yes {access_request_id}")
        assert "valid request" in mocked_testbot.pop_message()
        assert "assign request" in mocked_testbot.pop_message()
        assert "Granting" in mocked_testbot.pop_message()

class Test_allow_role_tag(ErrBotExtraTestSettings):
    @pytest.fixture
    def mocked_testbot_allow_true(self, testbot):
        config = create_config()
        config['ALLOW_ROLE_TAG'] = "allow-role"
        return inject_mocks(testbot, config, role_tags={'allow-role': True})

    @pytest.fixture
    def mocked_testbot_allow_false(self, testbot):
        config = create_config()
        config['ALLOW_ROLE_TAG'] = "allow-role"
        return inject_mocks(testbot, config, role_tags={'allow-role': False})

    @pytest.fixture
    def mocked_testbot_allow_group(self, testbot):
        config = create_config()
        config['GROUPS_TAG'] = "groups"
        config['ALLOW_ROLE_GROUPS_TAG'] = "allow-groups"
        return inject_mocks(testbot, config, role_tags={'allow-groups': 'a-group'}, account_tags={'groups': 'a-group'})

    def test_access_command_fail_for_not_allowed_roles(self, mocked_testbot_allow_false):
        mocked_testbot_allow_false.push_message("access to role Xxx")
        assert "not available" in mocked_testbot_allow_false.pop_message()

    def test_access_command_grant_when_allowed_role(self, mocked_testbot_allow_true):
        mocked_testbot_allow_true.push_message("access to role Xxx")
        mocked_testbot_allow_true.push_message(f"yes {access_request_id}")
        assert "valid request" in mocked_testbot_allow_true.pop_message()
        assert "assign request" in mocked_testbot_allow_true.pop_message()
        assert "Granting" in mocked_testbot_allow_true.pop_message()

    def test_access_command_grant_when_match_allowed_group(self, mocked_testbot_allow_group):
        mocked_testbot_allow_group.push_message("access to role Xxx")
        mocked_testbot_allow_group.push_message(f"yes {access_request_id}")
        assert "valid request" in mocked_testbot_allow_group.pop_message()
        assert "assign request" in mocked_testbot_allow_group.pop_message()
        assert "Granting" in mocked_testbot_allow_group.pop_message()

# pylint: disable=dangerous-default-value
def inject_mocks(testbot, config, roles = [], account_tags = None, throw_no_role_found = False, role_tags = None, role_grant_exists = False):
    accessbot = testbot.bot.plugin_manager.plugins['AccessBot']
    accessbot.config = config
    accessbot.build_identifier = MagicMock(return_value = get_dummy_person(account_name))
    accessbot.get_admins = MagicMock(return_value = ["gbin@localhost"])
    accessbot.get_api_access_key = MagicMock(return_value = "api-access_key")
    accessbot.get_api_secret_key = MagicMock(return_value = "c2VjcmV0LWtleQ==") # valid base64 string
    accessbot.get_sdm_service = MagicMock(return_value = create_sdm_service_mock(roles, account_tags, throw_no_role_found, role_tags, role_grant_exists))
    accessbot.get_role_grant_helper = MagicMock(return_value = create_role_grant_helper(accessbot))
    accessbot.get_approve_helper = MagicMock(return_value = create_approve_helper(accessbot))
    return testbot

def create_role_grant_helper(accessbot):
    helper = RoleGrantHelper(accessbot)
    helper.generate_grant_request_id = MagicMock(return_value = access_request_id)
    return helper

def create_approve_helper(accessbot):
    return ApproveHelper(accessbot)

def create_sdm_service_mock(roles, account_tags, throw_no_role_found, role_tags, role_grant_exists):
    service_mock = MagicMock()
    if throw_no_role_found:
        service_mock.get_role_by_name = MagicMock(side_effect = raise_no_role_found)
    else:
        service_mock.get_role_by_name = MagicMock(return_value = create_mock_role(role_tags))
    service_mock.get_account_by_email = MagicMock(return_value = create_mock_account(account_tags))
    service_mock.get_all_resources_by_role = MagicMock(return_value = create_mock_resources())
    service_mock.account_grant_exists = MagicMock(return_value = False)
    service_mock.get_granted_resources_via_account = MagicMock(return_value = [])
    service_mock.get_granted_resources_via_role = MagicMock(return_value = create_mock_resources()) if role_grant_exists else MagicMock(return_value=[])
    service_mock.get_all_roles = MagicMock(return_value = roles)
    return service_mock

def create_mock_account(tags):
    mock_account = MagicMock()
    mock_account.id = account_id
    mock_account.name = account_name
    mock_account.email = account_name
    mock_account.tags = tags
    return mock_account

def create_mock_role(tags):
    mock_role = MagicMock()
    mock_role.id = role_id
    mock_role.name = role_name
    mock_role.tags = tags
    return mock_role

def create_mock_resources():
    mock_resource = MagicMock()
    mock_resource.id = resource_id
    mock_resource.name = resource_name
    return [mock_resource]

def raise_no_role_found(message = '', match = ''):
    raise NotFoundException('Sorry, cannot find that role!')
