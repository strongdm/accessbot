# pylint: disable=invalid-name
import sys
import pytest
import time
from unittest.mock import MagicMock

sys.path.append('plugins/sdm')
sys.path.append('e2e/')

from test_common import create_config, DummyResource, send_message_override, callback_message_fn
from lib import ApproveHelper, ResourceGrantHelper, PollerHelper

pytest_plugins = ["errbot.backends.test"]
extra_plugin_dir = 'plugins/sdm'

resource_id = 1
resource_name = "myresource"
account_id = 1
account_name = "myaccount@test.com"
access_request_id = "12ab"
alternative_email_tag = "sdm_email"
alternative_email = "myemail001@email.com"

class Test_default_flow:  # manual approval
    @pytest.fixture
    def mocked_testbot(self, testbot):
        config = create_config()
        return inject_config(testbot, config)

    def test_access_command_grant_denied(self, mocked_testbot):
        push_access_request(mocked_testbot)
        mocked_testbot.push_message(f"no {access_request_id}")
        assert "valid request" in mocked_testbot.pop_message()
        assert "access request" in mocked_testbot.pop_message()
        assert "request has been denied" in mocked_testbot.pop_message()

    def test_access_command_grant_denied_with_reason(self, mocked_testbot):
        push_access_request(mocked_testbot)
        denial_reason = 'this is a denial reason'
        mocked_testbot.push_message(f"no {access_request_id} {denial_reason}")
        assert "valid request" in mocked_testbot.pop_message()
        assert "access request" in mocked_testbot.pop_message()
        denied_response_message = mocked_testbot.pop_message()
        assert "request has been denied" in denied_response_message
        assert "with the following reason" in denied_response_message
        assert denial_reason in denied_response_message

class Test_invalid_user:
    @pytest.fixture
    def mocked_testbot(self, testbot):
        config = create_config()
        config['SENDER_NICK_OVERRIDE'] = 'not-admin'
        return inject_config(testbot, config)

    def test_deny_command_fail_when_user_not_admin(self, mocked_testbot):
        push_access_request(mocked_testbot)
        mocked_testbot.push_message(f"no {access_request_id}")
        assert "valid request" in mocked_testbot.pop_message()
        assert "access request" in mocked_testbot.pop_message()
        assert "Invalid user" in mocked_testbot.pop_message()

class Test_invalid_request_id:
    @pytest.fixture
    def mocked_testbot(self, testbot):
        config = create_config()
        config['SENDER_NICK_OVERRIDE'] = 'not-admin'
        return inject_config(testbot, config)

    def test_deny_command_fail_when_request_id_is_invalid(self, mocked_testbot):
        push_access_request(mocked_testbot)
        mocked_testbot.push_message(f"no xxxx")
        assert "valid request" in mocked_testbot.pop_message()
        assert "access request" in mocked_testbot.pop_message()
        assert "Invalid access request" in mocked_testbot.pop_message()

# pylint: disable=dangerous-default-value
def inject_config(testbot, config, admins=["gbin@localhost"], tags={}, resources_by_role=[], account_grant_exists=False, resources=[], alternate_email = False):
    accessbot = testbot.bot.plugin_manager.plugins['AccessBot']
    accessbot.config = config
    accessbot.get_admins = MagicMock(return_value = admins)
    accessbot.get_api_access_key = MagicMock(return_value = "api-access_key")
    accessbot.get_api_secret_key = MagicMock(return_value = "c2VjcmV0LWtleQ==")  # valid base64 string
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

def create_account_mock(account_email = account_name):
    mock = MagicMock()
    mock.id = account_id
    mock.name = account_name
    mock.email = account_email
    return mock

def push_access_request(testbot):
    testbot.push_message("access to Xxx")
    # gives some time to process
    # needed in slow environments, e.g. github actions
    time.sleep(0.2)
