# pylint: disable=invalid-name
import datetime
import sys
import pytest
import time
from unittest.mock import MagicMock, patch

from test_common import create_config, DummyResource, send_message_override
sys.path.append('plugins/sdm')
from lib import ApproveHelper, ResourceGrantHelper, PollerHelper
from lib.exceptions import NotFoundException

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
        push_access_request(mocked_testbot)
        mocked_testbot.push_message(f"yes {access_request_id}")
        assert "valid request" in mocked_testbot.pop_message()
        assert "access request" in mocked_testbot.pop_message()
        assert "Granting" in mocked_testbot.pop_message()

    def test_access_command_grant_timed_out(self, mocked_testbot):
        push_access_request(mocked_testbot)
        assert "valid request" in mocked_testbot.pop_message()
        assert "access request" in mocked_testbot.pop_message()
        assert "timed out" in mocked_testbot.pop_message()
        assert "not approved" in mocked_testbot.pop_message()

    def test_access_command_grant_not_approved(self, mocked_testbot):
        push_access_request(mocked_testbot)
        mocked_testbot.push_message("no") # Anything but yes
        assert "valid request" in mocked_testbot.pop_message()
        assert "access request" in mocked_testbot.pop_message()
        assert "timed out" in mocked_testbot.pop_message()
        assert "not approved" in mocked_testbot.pop_message()

    def test_access_command_grant_bolded_yes_message(self, mocked_testbot):
        push_access_request(mocked_testbot)
        mocked_testbot.push_message(f"**yes {access_request_id}**")
        assert "valid request" in mocked_testbot.pop_message()
        assert "access request" in mocked_testbot.pop_message()
        assert "Granting" in mocked_testbot.pop_message()

    def test_access_command_grant_bolded_request_id_in_yes_message(self, mocked_testbot):
        push_access_request(mocked_testbot)
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

class Test_invalid_approver:
    @pytest.fixture
    def mocked_testbot(self, testbot):
        config = create_config()
        config['SENDER_NICK_OVERRIDE'] = 'not-admin'
        return inject_config(testbot, config)

    def test_access_command_fail_when_user_not_admin(self, mocked_testbot):
        push_access_request(mocked_testbot)
        mocked_testbot.push_message(f"yes {access_request_id}")
        assert "valid request" in mocked_testbot.pop_message()
        assert "access request" in mocked_testbot.pop_message()
        assert "Invalid approver" in mocked_testbot.pop_message()

class Test_auto_approve_all:
    @pytest.fixture
    def mocked_testbot(self, testbot):
        config = create_config()
        config['AUTO_APPROVE_ALL'] = True
        return inject_config(testbot, config)

    @pytest.fixture
    def mocked_with_max_auto_approve(self, mocked_testbot):
        accessbot = mocked_testbot.bot.plugin_manager.plugins['AccessBot']
        accessbot.config['MAX_AUTO_APPROVE_USES'] = 1
        accessbot.config['MAX_AUTO_APPROVE_INTERVAL'] = 1
        return mocked_testbot

    def test_auto_all(self, mocked_testbot):
        push_access_request(mocked_testbot)
        assert "Granting" in mocked_testbot.pop_message()

    def test_with_remaining_approvals_message(self, mocked_with_max_auto_approve):
        push_access_request(mocked_with_max_auto_approve)
        assert "Granting" in mocked_with_max_auto_approve.pop_message()
        assert "remaining" in mocked_with_max_auto_approve.pop_message()

    def test_default_flow_once_exhausted_auto_approvals(self, mocked_with_max_auto_approve):
        push_access_request(mocked_with_max_auto_approve)
        assert "Granting" in mocked_with_max_auto_approve.pop_message()
        assert "remaining" in mocked_with_max_auto_approve.pop_message()
        push_access_request(mocked_with_max_auto_approve)
        mocked_with_max_auto_approve.push_message(f"yes {access_request_id}")
        assert "valid request" in mocked_with_max_auto_approve.pop_message()
        assert "access request" in mocked_with_max_auto_approve.pop_message()
        assert "Granting" in mocked_with_max_auto_approve.pop_message()

    def test_keep_remaining_approvals_when_cleaner_passes(self, mocked_with_max_auto_approve):
        push_access_request(mocked_with_max_auto_approve)
        assert "Granting" in mocked_with_max_auto_approve.pop_message()
        assert "remaining" in mocked_with_max_auto_approve.pop_message()
        accessbot = mocked_with_max_auto_approve.bot.plugin_manager.plugins['AccessBot']
        PollerHelper(accessbot).stale_max_auto_approve_cleaner()
        push_access_request(mocked_with_max_auto_approve)
        assert "Granting" in mocked_with_max_auto_approve.pop_message()
        assert "remaining" in mocked_with_max_auto_approve.pop_message()

class Test_multiple_admins_flow:
    @pytest.fixture
    def mocked_testbot(self, testbot):
        config = create_config()
        return inject_config(testbot, config, admins = ["gbin@localhost",  "user1"])

    def test_access_command_grant_multiple_admins(self, mocked_testbot):
        push_access_request(mocked_testbot)
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
        push_access_request(mocked_testbot)
        assert "Granting" in mocked_testbot.pop_message()

class Test_hide_resource_tag:
    @pytest.fixture
    def mocked_testbot_hide_true(self, testbot):
        config = create_config()
        config['HIDE_RESOURCE_TAG'] = "hide-resource"
        return inject_config(testbot, config, tags = {'hide-resource': True})

    @pytest.fixture
    def mocked_testbot_hide_false(self, testbot):
        config = create_config()
        config['HIDE_RESOURCE_TAG'] = "hide-resource"
        return inject_config(testbot, config, tags = {'hide-resource': False})

    def test_access_command_fail_for_hidden_resources(self, mocked_testbot_hide_true):
        push_access_request(mocked_testbot_hide_true)
        assert "not available" in mocked_testbot_hide_true.pop_message()

    def test_access_command_grant_when_hide_resource_is_false(self, mocked_testbot_hide_false):
        push_access_request(mocked_testbot_hide_false)
        mocked_testbot_hide_false.push_message(f"yes {access_request_id}")
        assert "valid request" in mocked_testbot_hide_false.pop_message()
        assert "access request" in mocked_testbot_hide_false.pop_message()
        assert "Granting" in mocked_testbot_hide_false.pop_message()

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
        grant_temporary_access_mock = accessbot.get_sdm_service().grant_temporary_access
        with patch('datetime.datetime', new = self.NewDate):
            push_access_request(mocked_testbot)
            mocked_testbot.push_message(f"yes {access_request_id}")
            assert "valid request" in mocked_testbot.pop_message()
            assert "access request" in mocked_testbot.pop_message()
            assert "Granting" in mocked_testbot.pop_message()

            start_from = datetime.datetime(2021, 5, 12, 0, 0)
            valid_until = datetime.datetime(2021, 5, 12, 0, 1)
            grant_temporary_access_mock.assert_called_with(resource_id, account_id, start_from, valid_until)

class Test_resources_by_role:
    @pytest.fixture
    def mocked_testbot(self, testbot):
        config = create_config()
        config['CONTROL_RESOURCES_ROLE_NAME'] = 'myrole'
        resources_by_role = [DummyResource("Xxx", {})]
        return inject_config(testbot, config, resources_by_role = resources_by_role)

    def test_access_command_grant_for_valid_resource(self, mocked_testbot):
        push_access_request(mocked_testbot)
        mocked_testbot.push_message(f"yes {access_request_id}")
        assert "valid request" in mocked_testbot.pop_message()
        assert "access request" in mocked_testbot.pop_message()
        assert "Granting" in mocked_testbot.pop_message()

    def test_access_command_fail_for_invalid_resource(self, mocked_testbot):
        mocked_testbot.push_message("access to Yyy")
        assert "not available" in mocked_testbot.pop_message()

class Test_acount_grant_exists:
    @pytest.fixture
    def mocked_testbot(self, testbot):
        config = create_config()
        return inject_config(testbot, config, account_grant_exists = True)

    def test_when_grant_exists(self, mocked_testbot):
        push_access_request(mocked_testbot)
        assert "already have access" in mocked_testbot.pop_message()

    def test_when_grant_doesnt_exists(self, mocked_testbot):
        accessbot = mocked_testbot.bot.plugin_manager.plugins['AccessBot']
        service = accessbot.get_sdm_service()
        service.account_grant_exists.return_value = False
        push_access_request(mocked_testbot)
        assert "valid request" in mocked_testbot.pop_message()
        assert "access request" in mocked_testbot.pop_message()

class Test_admin_in_channel:
    channel_name = 'testroom'
    raw_messages = []

    @pytest.fixture
    def mocked_testbot(self, testbot):
        config = create_config()
        config['ADMINS_CHANNEL'] = f"#{self.channel_name}"
        testbot.bot.send_message = send_message_override(testbot.bot, self.raw_messages)
        return inject_config(testbot, config)

    def test_access_command_grant_for_valid_sender_room(self, mocked_testbot):
        mocked_testbot.bot.sender.room = create_room_mock(self.channel_name)
        push_access_request(mocked_testbot)
        mocked_testbot.push_message(f"yes {access_request_id}")
        assert "valid request" in mocked_testbot.pop_message()
        assert "access request" in mocked_testbot.pop_message()
        assert "Granting" in mocked_testbot.pop_message()
        assert self.raw_messages[1].to.person == f"#{self.channel_name}"

    def test_access_command_fails_for_invalid_sender_room(self, mocked_testbot):
        push_access_request(mocked_testbot)
        mocked_testbot.push_message(f"yes {access_request_id}")
        assert "valid request" in mocked_testbot.pop_message()
        assert "access request" in mocked_testbot.pop_message()
        assert "Invalid approver" in mocked_testbot.pop_message()


# pylint: disable=dangerous-default-value
class Test_fuzzy_matching:
    resource_name = "Very Long name"

    @pytest.fixture
    def mocked_testbot(self, testbot):
        config = create_config()
        resources = [ DummyResource(self.resource_name, {}) ]
        return inject_config(testbot, config, resources = resources)

    def test_find_fuzzy_matching(self, mocked_testbot):
        mocked_testbot.push_message("access to Long name")
        time.sleep(0.2)
        assert "cannot find that resource" in mocked_testbot.pop_message()
        recommendation = mocked_testbot.pop_message()
        assert "Did you mean" in recommendation
        assert self.resource_name in recommendation

    def test_fail_find_fuzzy_matching(self, mocked_testbot):
        mocked_testbot.push_message("access to name") # it's to short, the threshold is not good enough
        time.sleep(0.2)
        assert "cannot find that resource" in mocked_testbot.pop_message()

# pylint: disable=dangerous-default-value
def inject_config(testbot, config, admins = ["gbin@localhost"], tags = {}, resources_by_role = [], account_grant_exists = False, resources = []):
    accessbot = testbot.bot.plugin_manager.plugins['AccessBot']
    accessbot.config = config
    accessbot.get_admins = MagicMock(return_value = admins)
    accessbot.get_api_access_key = MagicMock(return_value = "api-access_key")
    accessbot.get_api_secret_key = MagicMock(return_value = "c2VjcmV0LWtleQ==") # valid base64 string
    accessbot.get_sdm_service = MagicMock(return_value = create_sdm_service_mock(tags, resources_by_role, account_grant_exists, resources))
    accessbot.get_resource_grant_helper = MagicMock(return_value = create_resource_grant_helper(accessbot))
    accessbot.get_approve_helper = MagicMock(return_value = create_approve_helper(accessbot))
    return testbot

def create_resource_grant_helper(accessbot):
    helper = ResourceGrantHelper(accessbot)
    helper.generate_grant_request_id = MagicMock(return_value = access_request_id)
    return helper

def create_approve_helper(accessbot):
    return ApproveHelper(accessbot)

def create_sdm_service_mock(tags, resources_by_role, account_grant_exists, resources):
    mock = MagicMock()
    if len(resources) > 0:
        mock.get_resource_by_name = MagicMock(side_effect = raise_no_resource_found)
    else:
        mock.get_resource_by_name = MagicMock(return_value = create_resource_mock(tags))
    mock.get_account_by_email = MagicMock(return_value = create_account_mock())
    mock.grant_temporary_access = MagicMock()
    mock.get_all_resources_by_role = MagicMock(return_value = resources_by_role)
    mock.account_grant_exists = MagicMock(return_value = account_grant_exists)
    mock.get_all_resources = MagicMock(return_value = resources)
    return mock

def create_resource_mock(tags):
    mock = MagicMock()
    mock.id = resource_id
    mock.name = resource_name
    mock.tags = tags
    return mock

def create_account_mock():
    mock = MagicMock()
    mock.id = account_id
    mock.name = account_name
    return mock

def create_room_mock(channel_name):
    mock = MagicMock()
    mock.name = channel_name
    return mock

def push_access_request(testbot):
    testbot.push_message("access to Xxx")
    # gives some time to process
    # needed in slow environments, e.g. github actions
    time.sleep(0.2)

def raise_no_resource_found(message = '', match = ''):
    raise NotFoundException('Sorry, cannot find that resource!')
