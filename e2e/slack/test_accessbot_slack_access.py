# pylint: disable=invalid-name
import datetime
import sys
import pytest
import time
from unittest.mock import MagicMock, patch

sys.path.append('plugins/sdm')
sys.path.append('e2e')

from test_common import create_config, DummyResource, send_message_override, \
    callback_message_fn, get_dummy_person, ErrBotExtraTestSettings, DummyPerson, DummyRoom
from lib import ApproveHelper, ResourceGrantHelper, PollerHelper
from lib.exceptions import NotFoundException

pytest_plugins = ["errbot.backends.test"]

resource_id = 1
resource_name = "myresource"
account_id = 1
account_name = "myaccount@test.com"
access_request_id = "12AB"
alternative_email_tag = "sdm_email"
alternative_email = "myemail001@email.com"
access_form_bot_id = "B0000000000"
room_id = "C00000000"
room_name = "myroom"
required_flags = "reason duration"

class Test_default_flow(ErrBotExtraTestSettings):  # manual approval
    @pytest.fixture
    def mocked_testbot(self, testbot):
        config = create_config()
        return inject_config(testbot, config)

    @pytest.fixture
    def mocked_testbot_with_no_admin_users(self, testbot):
        config = create_config()
        testbot.bot.send_message = send_message_override(testbot.bot, [])
        testbot.bot.plugin_manager.plugins['AccessBot'].get_admin_ids = MagicMock(
            return_value=[get_dummy_person(account_name, is_deleted=True)]
        )
        return inject_config(testbot, config)

    @pytest.fixture
    def mocked_testbot_with_required_flags(self, mocked_testbot):
        accessbot = mocked_testbot.bot.plugin_manager.plugins['AccessBot']
        accessbot.config['REQUIRED_FLAGS'] = required_flags
        return mocked_testbot

    def test_access_command_grant_approved(self, mocked_testbot):
        mocked_testbot.push_message("access to Xxx")
        mocked_testbot.push_message(f"yes {access_request_id}")
        assert "valid request" in mocked_testbot.pop_message()
        assert "access request" in mocked_testbot.pop_message()
        assert "Granting" in mocked_testbot.pop_message()

    def test_access_command_grant_timed_out(self, mocked_testbot):
        mocked_testbot.push_message("access to Xxx")
        time.sleep(0.1)
        assert "valid request" in mocked_testbot.pop_message()
        assert "access request" in mocked_testbot.pop_message()
        assert "timed out" in mocked_testbot.pop_message()
        assert "not approved" in mocked_testbot.pop_message()

    def test_access_command_grant_not_approved(self, mocked_testbot):
        mocked_testbot.push_message("access to Xxx")
        mocked_testbot.push_message("no")  # Anything but yes
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

    def test_access_command_grant_access_with_reason_message(self, mocked_testbot):
        request_reason = 'please, accept this request'
        mocked_testbot.push_message(f"access to Xxx --reason {request_reason}")
        mocked_testbot.push_message(f"yes {access_request_id}")
        assert "valid request" in mocked_testbot.pop_message()
        request_message = mocked_testbot.pop_message()
        assert "access request" in request_message
        assert request_reason in request_message
        assert "Granting" in mocked_testbot.pop_message()

    def test_access_command_dont_grant_access_when_reason_flag_has_no_value(self, mocked_testbot):
        mocked_testbot.push_message(f"access to Xxx --reason")
        assert "You need to enter a valid reason" in mocked_testbot.pop_message()

    def test_access_command_grant_access_with_duration_flag(self, mocked_testbot):
        duration = '45'
        mocked_testbot.push_message(f"access to Xxx --duration {duration}")
        mocked_testbot.push_message(f"yes {access_request_id}")
        assert "valid request" in mocked_testbot.pop_message()
        request_message = mocked_testbot.pop_message()
        assert "access request" in request_message
        assert f"{duration} minutes" in request_message
        assert "Granting" in mocked_testbot.pop_message()

    def test_access_command_grant_access_with_duration_flag_with_minutes(self, mocked_testbot):
        duration = '45'
        short_unit = 'm'
        full_unit = 'minutes'
        mocked_testbot.push_message(f"access to Xxx --duration {duration}{short_unit}")
        mocked_testbot.push_message(f"yes {access_request_id}")
        assert "valid request" in mocked_testbot.pop_message()
        request_message = mocked_testbot.pop_message()
        assert "access request" in request_message
        assert f"{duration} {full_unit}" in request_message
        assert "Granting" in mocked_testbot.pop_message()

    def test_access_command_grant_access_with_duration_flag_with_hours(self, mocked_testbot):
        duration = '6'
        short_unit = 'h'
        full_unit = 'hours'
        mocked_testbot.push_message(f"access to Xxx --duration {duration}{short_unit}")
        mocked_testbot.push_message(f"yes {access_request_id}")
        assert "valid request" in mocked_testbot.pop_message()
        request_message = mocked_testbot.pop_message()
        assert "access request" in request_message
        assert f"{duration} {full_unit}" in request_message
        assert "Granting" in mocked_testbot.pop_message()

    def test_access_command_grant_access_with_duration_flag_with_days(self, mocked_testbot):
        duration = '2'
        short_unit = 'd'
        full_unit = 'days'
        mocked_testbot.push_message(f"access to Xxx --duration {duration}{short_unit}")
        mocked_testbot.push_message(f"yes {access_request_id}")
        assert "valid request" in mocked_testbot.pop_message()
        request_message = mocked_testbot.pop_message()
        assert "access request" in request_message
        assert f"{duration} {full_unit}" in request_message
        assert "Granting" in mocked_testbot.pop_message()

    def test_access_command_grant_access_with_duration_flag_with_weeks(self, mocked_testbot):
        duration = '3'
        short_unit = 'w'
        full_unit = 'weeks'
        mocked_testbot.push_message(f"access to Xxx --duration {duration}{short_unit}")
        mocked_testbot.push_message(f"yes {access_request_id}")
        assert "valid request" in mocked_testbot.pop_message()
        request_message = mocked_testbot.pop_message()
        assert "access request" in request_message
        assert f"{duration} {full_unit}" in request_message
        assert "Granting" in mocked_testbot.pop_message()

    def test_access_command_grant_access_with_duration_flag_with_converted_units(self, mocked_testbot):
        duration = '90'
        short_unit = 'm'
        converted_duration = '1 hours 30 minutes'
        mocked_testbot.push_message(f"access to Xxx --duration {duration}{short_unit}")
        mocked_testbot.push_message(f"yes {access_request_id}")
        assert "valid request" in mocked_testbot.pop_message()
        request_message = mocked_testbot.pop_message()
        assert "access request" in request_message
        assert converted_duration in request_message
        assert "Granting" in mocked_testbot.pop_message()

    def test_access_command_dont_grant_access_when_empty_duration_flag(self, mocked_testbot):
        mocked_testbot.push_message(f"access to Xxx --duration")
        assert "You need to enter a valid duration" in mocked_testbot.pop_message()

    def test_access_command_dont_grant_access_when_duration_flag_has_invalid_unit(self, mocked_testbot):
        duration = '30'
        invalid_unit = 'x'
        mocked_testbot.push_message(f"access to Xxx --duration {duration}{invalid_unit}")
        invalid_unit_message = mocked_testbot.pop_message()
        assert "You need to enter a valid duration unit" in invalid_unit_message
        assert "Valid units are: m, h, d, w" in invalid_unit_message

    def test_access_command_dont_grant_access_when_duration_flag_has_duration_equals_to_zero(self, mocked_testbot):
        duration = '0'
        mocked_testbot.push_message(f"access to Xxx --duration {duration}")
        assert "You need to enter a duration greater than zero" in mocked_testbot.pop_message()

    def test_access_command_fails_for_unreachable_admin_users(self, mocked_testbot_with_no_admin_users):
        mocked_testbot_with_no_admin_users.push_message("access to Xxx")
        assert "no active Slack Admin" in mocked_testbot_with_no_admin_users.pop_message()

    def test_access_command_grant_access_when_using_required_flags(self, mocked_testbot_with_required_flags):
        mocked_testbot_with_required_flags.push_message(f"access to Xxx --reason my reason --duration 15m")
        mocked_testbot_with_required_flags.push_message(f"yes {access_request_id}")
        assert "valid request" in mocked_testbot_with_required_flags.pop_message()
        assert "access request" in mocked_testbot_with_required_flags.pop_message()
        assert "Granting" in mocked_testbot_with_required_flags.pop_message()

    def test_access_command_fails_when_missing_required_flags(self, mocked_testbot_with_required_flags):
        mocked_testbot_with_required_flags.push_message(f"access to Xxx")
        request_message = mocked_testbot_with_required_flags.pop_message()
        assert "Missing required flags" in request_message
        assert "reason" in request_message
        assert "duration" in request_message

    def test_access_command_fails_when_partially_missing_required_flags(self, mocked_testbot_with_required_flags):
        mocked_testbot_with_required_flags.push_message(f"access to Xxx --reason my reason")
        request_message = mocked_testbot_with_required_flags.pop_message()
        assert "Missing required flags" in request_message
        assert "reason" not in request_message
        assert "duration" in request_message

    def test_access_command_grant_with_strange_casing(self, mocked_testbot):
        mocked_testbot.push_message("AcCesS TO Xxx")
        mocked_testbot.push_message(f"YeS 12aB")
        assert "valid request" in mocked_testbot.pop_message()
        assert "access request" in mocked_testbot.pop_message()
        assert "Granting" in mocked_testbot.pop_message()

class Test_access_flow_from_access_form(ErrBotExtraTestSettings):

    @pytest.fixture
    def mocked_testbot(self, testbot):
        config = create_config()
        config['SENDER_NICK_OVERRIDE'] = None
        config['SENDER_EMAIL_OVERRIDE'] = None
        bot = inject_config(testbot, config, admins=['@admin'])
        bot.bot.plugin_manager.plugins['AccessBot'].build_identifier = MagicMock(side_effect=mocked_build_identifier_with_nick)
        return bot

    def test_access_command_from_access_form_bot(self, mocked_testbot):
        mocked_testbot._bot.callback_message = MagicMock(side_effect=callback_message_fn(
            mocked_testbot._bot,
            bot_id=access_form_bot_id,
            room_id=room_id,
            room_name=room_name
        ))
        mocked_testbot._bot.bot_config.ACCESS_FORM_BOT_INFO['bot_id'] = access_form_bot_id
        mocked_testbot.push_message(f"access to Xxx --requester @user")
        ack_message = mocked_testbot.pop_message()
        assert "Thanks `@user`" in ack_message
        assert "valid request" in ack_message
        mocked_testbot._bot.callback_message = MagicMock(side_effect=callback_message_fn(
            mocked_testbot._bot,
            from_nick="admin"
        ))
        mocked_testbot.push_message(f"yes {access_request_id}")
        request_message = mocked_testbot.pop_message()
        assert "access request" in request_message
        assert "Granting" in mocked_testbot.pop_message()
        mocked_testbot._bot.bot_config.ACCESS_FORM_BOT_INFO['bot_id'] = None

    def test_access_command_fails_when_user_cannot_use_requester_flag(self, mocked_testbot):
        mocked_testbot._bot.callback_message = MagicMock(side_effect=callback_message_fn(
            mocked_testbot._bot
        ))
        mocked_testbot.push_message(f"access to Xxx --requester @user")
        assert "You cannot use the requester flag." in mocked_testbot.pop_message()

class Test_invalid_approver(ErrBotExtraTestSettings):
    @pytest.fixture
    def mocked_testbot(self, testbot):
        config = create_config()
        config['SENDER_NICK_OVERRIDE'] = 'not-admin'
        return inject_config(testbot, config)

    def test_access_command_fail_when_user_not_admin(self, mocked_testbot):
        mocked_testbot.push_message("access to Xxx")
        mocked_testbot.push_message(f"yes {access_request_id}")
        assert "valid request" in mocked_testbot.pop_message()
        assert "access request" in mocked_testbot.pop_message()
        assert "Invalid user" in mocked_testbot.pop_message()

class Test_auto_approve_all(ErrBotExtraTestSettings):
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
        mocked_testbot.push_message("access to Xxx")
        assert "Granting" in mocked_testbot.pop_message()

    def test_with_remaining_approvals_message(self, mocked_with_max_auto_approve):
        mocked_with_max_auto_approve.push_message("access to Xxx")
        assert "Granting" in mocked_with_max_auto_approve.pop_message()
        assert "remaining" in mocked_with_max_auto_approve.pop_message()

    def test_default_flow_once_exhausted_auto_approvals(self, mocked_with_max_auto_approve):
        mocked_with_max_auto_approve.push_message("access to Xxx")
        assert "Granting" in mocked_with_max_auto_approve.pop_message()
        assert "remaining" in mocked_with_max_auto_approve.pop_message()
        mocked_with_max_auto_approve.push_message("access to Xxx")
        mocked_with_max_auto_approve.push_message(f"yes {access_request_id}")
        assert "valid request" in mocked_with_max_auto_approve.pop_message()
        assert "access request" in mocked_with_max_auto_approve.pop_message()
        assert "Granting" in mocked_with_max_auto_approve.pop_message()

    def test_keep_remaining_approvals_when_cleaner_passes(self, mocked_with_max_auto_approve):
        mocked_with_max_auto_approve.push_message("access to Xxx")
        assert "Granting" in mocked_with_max_auto_approve.pop_message()
        assert "remaining" in mocked_with_max_auto_approve.pop_message()
        accessbot = mocked_with_max_auto_approve.bot.plugin_manager.plugins['AccessBot']
        PollerHelper(accessbot).stale_max_auto_approve_cleaner()
        mocked_with_max_auto_approve.push_message("access to Xxx")
        assert "Granting" in mocked_with_max_auto_approve.pop_message()
        assert "remaining" in mocked_with_max_auto_approve.pop_message()

class Test_multiple_admins_flow(ErrBotExtraTestSettings):
    @pytest.fixture
    def mocked_testbot(self, testbot):
        config = create_config()
        return inject_config(testbot, config, admins=["gbin@localhost", "user1"])

    def test_access_command_grant_multiple_admins(self, mocked_testbot):
        mocked_testbot.push_message("access to Xxx")
        mocked_testbot.push_message(f"yes {access_request_id}")
        assert "valid request" in mocked_testbot.pop_message()
        assert "access request" in mocked_testbot.pop_message()
        assert "access request" in mocked_testbot.pop_message()
        assert "Granting" in mocked_testbot.pop_message()

class Test_auto_approve_tag(ErrBotExtraTestSettings):
    @pytest.fixture
    def mocked_testbot(self, testbot):
        config = create_config()
        config['AUTO_APPROVE_TAG'] = "auto-approve"
        return inject_config(testbot, config, tags={'auto-approve': True})

    def test_access_command_grant_auto_approved_for_tagged_resource(self, mocked_testbot):
        mocked_testbot.push_message("access to Xxx")
        assert "Granting" in mocked_testbot.pop_message()

class Test_auto_approve_groups_tag(ErrBotExtraTestSettings):

    @pytest.fixture
    def mocked_testbot_with_intersecting_groups(self, testbot):
        config = create_config()
        config['AUTO_APPROVE_GROUPS_TAG'] = "auto-approve-groups"
        config['GROUPS_TAG'] = "groups"
        return inject_config(testbot, config, tags={'auto-approve-groups': 'test-group'},
                             account_tags={'groups': 'test-group'})

    @pytest.fixture
    def mocked_testbot_with_non_intersecting_groups(self, testbot):
        config = create_config()
        config['AUTO_APPROVE_GROUPS_TAG'] = "auto-approve-groups"
        config['GROUPS_TAG'] = "groups"
        return inject_config(testbot, config, tags={'auto-approve-groups': 'another-group'},
                             account_tags={'groups': 'test-group'})

    def test_auto_approve_for_intersecting_group(self, mocked_testbot_with_intersecting_groups):
        mocked_testbot_with_intersecting_groups.push_message("access to Xxx")
        assert "Granting" in mocked_testbot_with_intersecting_groups.pop_message()

    def test_dont_auto_approve_for_non_intersecting_groups(self, mocked_testbot_with_non_intersecting_groups):
        mocked_testbot_with_non_intersecting_groups.push_message("access to Xxx")
        assert "valid request" in mocked_testbot_with_non_intersecting_groups.pop_message()
        assert "access request" in mocked_testbot_with_non_intersecting_groups.pop_message()

class Test_allow_resource_tag(ErrBotExtraTestSettings):
    @pytest.fixture
    def mocked_testbot_allow_true(self, testbot):
        config = create_config()
        config['ALLOW_RESOURCE_TAG'] = "allow-resource"
        return inject_config(testbot, config, tags={'allow-resource': True})

    @pytest.fixture
    def mocked_testbot_allow_false(self, testbot):
        config = create_config()
        config['ALLOW_RESOURCE_TAG'] = "allow-resource"
        return inject_config(testbot, config, tags={'allow-resource': False})

    def test_access_command_fail_for_not_allowed_resources(self, mocked_testbot_allow_false):
        mocked_testbot_allow_false.push_message("access to Xxx")
        assert "not available" in mocked_testbot_allow_false.pop_message()

    def test_access_command_grant_when_allowed_resource(self, mocked_testbot_allow_true):
        mocked_testbot_allow_true.push_message("access to Xxx")
        mocked_testbot_allow_true.push_message(f"yes {access_request_id}")
        assert "valid request" in mocked_testbot_allow_true.pop_message()
        assert "access request" in mocked_testbot_allow_true.pop_message()
        assert "Granting" in mocked_testbot_allow_true.pop_message()

class Test_hide_resource_tag(ErrBotExtraTestSettings):
    @pytest.fixture
    def mocked_testbot_hide_true(self, testbot):
        config = create_config()
        config['HIDE_RESOURCE_TAG'] = "hide-resource"
        return inject_config(testbot, config, tags={'hide-resource': True})

    @pytest.fixture
    def mocked_testbot_hide_false(self, testbot):
        config = create_config()
        config['HIDE_RESOURCE_TAG'] = "hide-resource"
        return inject_config(testbot, config, tags={'hide-resource': False})

    def test_access_command_fail_for_hidden_resources(self, mocked_testbot_hide_true):
        mocked_testbot_hide_true.push_message("access to Xxx")
        assert "not available" in mocked_testbot_hide_true.pop_message()

    def test_access_command_grant_when_hide_resource_is_false(self, mocked_testbot_hide_false):
        mocked_testbot_hide_false.push_message("access to Xxx")
        mocked_testbot_hide_false.push_message(f"yes {access_request_id}")
        assert "valid request" in mocked_testbot_hide_false.pop_message()
        assert "access request" in mocked_testbot_hide_false.pop_message()
        assert "Granting" in mocked_testbot_hide_false.pop_message()

class Test_conceal_resource_tag(ErrBotExtraTestSettings):
    @pytest.fixture
    def mocked_testbot_conceal_true(self, testbot):
        config = create_config()
        config['CONCEAL_RESOURCE_TAG'] = "conceal-resource"
        return inject_config(testbot, config, tags={'conceal-resource': True})

    @pytest.fixture
    def mocked_testbot_conceal_false(self, testbot):
        config = create_config()
        config['CONCEAL_RESOURCE_TAG'] = "conceal-resource"
        return inject_config(testbot, config, tags={'conceal-resource': False})

    def test_access_command_fail_for_hidden_resources(self, mocked_testbot_conceal_true):
        mocked_testbot_conceal_true.push_message("access to Xxx")
        mocked_testbot_conceal_true.push_message(f"yes {access_request_id}")
        assert "valid request" in mocked_testbot_conceal_true.pop_message()
        assert "access request" in mocked_testbot_conceal_true.pop_message()
        assert "Granting" in mocked_testbot_conceal_true.pop_message()

    def test_access_command_grant_when_conceal_resource_is_false(self, mocked_testbot_conceal_false):
        mocked_testbot_conceal_false.push_message("access to Xxx")
        mocked_testbot_conceal_false.push_message(f"yes {access_request_id}")
        assert "valid request" in mocked_testbot_conceal_false.pop_message()
        assert "access request" in mocked_testbot_conceal_false.pop_message()
        assert "Granting" in mocked_testbot_conceal_false.pop_message()

class Test_grant_timeout(ErrBotExtraTestSettings):
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
        with patch('datetime.datetime', new=self.NewDate):
            mocked_testbot.push_message("access to Xxx")
            mocked_testbot.push_message(f"yes {access_request_id}")
            assert "valid request" in mocked_testbot.pop_message()
            assert "access request" in mocked_testbot.pop_message()
            assert "Granting" in mocked_testbot.pop_message()

            start_from = datetime.datetime(2021, 5, 12, 0, 0)
            valid_until = datetime.datetime(2021, 5, 12, 0, 1)
            grant_temporary_access_mock.assert_called_with(resource_id, account_id, start_from, valid_until)

class Test_resources_by_role(ErrBotExtraTestSettings):
    @pytest.fixture
    def mocked_testbot(self, testbot):
        config = create_config()
        config['CONTROL_RESOURCES_ROLE_NAME'] = 'myrole'
        resources_by_role = [DummyResource("Xxx", {})]
        return inject_config(testbot, config, resources_by_role=resources_by_role)

    def test_access_command_grant_for_valid_resource(self, mocked_testbot):
        mocked_testbot.push_message("access to Xxx")
        mocked_testbot.push_message(f"yes {access_request_id}")
        assert "valid request" in mocked_testbot.pop_message()
        assert "access request" in mocked_testbot.pop_message()
        assert "Granting" in mocked_testbot.pop_message()

    def test_access_command_fail_for_invalid_resource(self, mocked_testbot):
        mocked_testbot.push_message("access to Yyy")
        assert "not available" in mocked_testbot.pop_message()

class Test_acount_grant_exists(ErrBotExtraTestSettings):
    @pytest.fixture
    def mocked_testbot(self, testbot):
        config = create_config()
        return inject_config(testbot, config, account_grant_exists=True)

    def test_when_grant_exists(self, mocked_testbot):
        mocked_testbot.push_message("access to Xxx")
        assert "already have access" in mocked_testbot.pop_message()

    def test_when_grant_doesnt_exists(self, mocked_testbot):
        accessbot = mocked_testbot.bot.plugin_manager.plugins['AccessBot']
        service = accessbot.get_sdm_service()
        service.account_grant_exists.return_value = False
        mocked_testbot.push_message("access to Xxx")
        assert "valid request" in mocked_testbot.pop_message()
        assert "access request" in mocked_testbot.pop_message()

class Test_admin_in_channel(ErrBotExtraTestSettings):
    channel_name = 'testroom'
    raw_messages = []

    @pytest.fixture
    def mocked_testbot_with_channels(self, testbot):
        config = create_config()
        config['ADMINS_CHANNEL'] = f"#{self.channel_name}"
        testbot.bot.send_message = send_message_override(testbot.bot, self.raw_messages)
        testbot.bot.channels = MagicMock(return_value=[{'name': self.channel_name, 'is_member': True}])
        return inject_config(testbot, config)

    @pytest.fixture
    def mocked_testbot_with_no_channels(self, testbot):
        config = create_config()
        config['ADMINS_CHANNEL'] = f"#{self.channel_name}"
        testbot.bot.send_message = send_message_override(testbot.bot, self.raw_messages)
        testbot.bot.channels = MagicMock(return_value=[])
        return inject_config(testbot, config)

    def test_access_command_grant_for_valid_sender_room(self, mocked_testbot_with_channels):
        mocked_testbot_with_channels.bot.plugin_manager.plugins['AccessBot'].build_identifier = MagicMock(
            return_value=get_dummy_person(f'#{self.channel_name}'))
        mocked_testbot_with_channels.bot.sender.room = create_room_mock(self.channel_name)
        mocked_testbot_with_channels.push_message("access to Xxx")
        mocked_testbot_with_channels.push_message(f"yes {access_request_id}")
        assert "valid request" in mocked_testbot_with_channels.pop_message()
        assert "access request" in mocked_testbot_with_channels.pop_message()
        assert "Granting" in mocked_testbot_with_channels.pop_message()
        assert self.raw_messages[1].to.person == f"#{self.channel_name}"

    def test_access_command_fails_for_invalid_sender_room(self, mocked_testbot_with_channels):
        mocked_testbot_with_channels.push_message("access to Xxx")
        mocked_testbot_with_channels.push_message(f"yes {access_request_id}")
        assert "valid request" in mocked_testbot_with_channels.pop_message()
        assert "access request" in mocked_testbot_with_channels.pop_message()
        assert "Invalid user" in mocked_testbot_with_channels.pop_message()

    def test_access_command_fails_for_unreachable_admin_channel(self, mocked_testbot_with_no_channels):
        mocked_testbot_with_no_channels.push_message("access to Xxx")
        mocked_testbot_with_no_channels.push_message(f"yes {access_request_id}")
        assert "but it's unreachable" in mocked_testbot_with_no_channels.pop_message()

class Test_fuzzy_matching(ErrBotExtraTestSettings):
    resource_name = "Very Long name"

    @pytest.fixture
    def mocked_testbot(self, testbot):
        config = create_config()
        resources = [DummyResource(self.resource_name, {})]
        return inject_config(testbot, config, resources=resources)

    def test_find_fuzzy_matching(self, mocked_testbot):
        mocked_testbot.push_message("access to Long name")
        assert "cannot find that resource" in mocked_testbot.pop_message()
        recommendation = mocked_testbot.pop_message()
        assert "Did you mean" in recommendation
        assert self.resource_name in recommendation

    def test_fail_find_fuzzy_matching(self, mocked_testbot):
        mocked_testbot.push_message("access to name")  # it's to short, the threshold is not good enough
        assert "cannot find that resource" in mocked_testbot.pop_message()

    def test_find_with_disabled_fuzzy_matching(self, mocked_testbot):
        accessbot = mocked_testbot.bot.plugin_manager.plugins['AccessBot']
        accessbot.config['ENABLE_RESOURCES_FUZZY_MATCHING'] = False
        mocked_testbot.push_message("access to Long name")
        assert "cannot find that resource" in mocked_testbot.pop_message()

# pylint: disable=protected-access
class Test_self_approve(ErrBotExtraTestSettings):
    channel_name = 'testroom'

    @pytest.fixture
    def mocked_testbot(self, testbot):
        config = create_config()
        config['ADMINS_CHANNEL'] = f"#{self.channel_name}"
        config['ADMIN_TIMEOUT'] = 30
        testbot.bot.sender.room = create_room_mock(self.channel_name)
        testbot.bot.sender._nick = config['SENDER_NICK_OVERRIDE']
        testbot.bot.sender._email = config['SENDER_EMAIL_OVERRIDE']
        testbot.bot.channels = MagicMock(return_value=[{'name': self.channel_name, 'is_member': True}])
        return inject_config(testbot, config, admins=[f'@not-admin'])

    def test_when_approver_is_not_the_requester(self, mocked_testbot):
        mocked_testbot.push_message("access to Xxx")
        mocked_testbot.push_message(f"yes {access_request_id}")
        assert "valid request" in mocked_testbot.pop_message()
        assert "access request" in mocked_testbot.pop_message()
        assert "Granting" in mocked_testbot.pop_message()

    def test_when_approver_is_requester(self, mocked_testbot):
        mocked_testbot.bot.sender._email = account_name
        mocked_testbot.bot.sender._nick = account_name
        mocked_testbot.push_message("access to Xxx")
        mocked_testbot.push_message(f"yes {access_request_id}")
        assert "valid request" in mocked_testbot.pop_message()
        assert "access request" in mocked_testbot.pop_message()
        assert "Invalid" in mocked_testbot.pop_message()

class Test_alternative_email(ErrBotExtraTestSettings):
    @pytest.fixture
    def mocked_user_profile(self):
        return {
            'fields': {
                'XXX': {
                    'label': alternative_email_tag,
                    'value': alternative_email,
                }
            }
        }

    @pytest.fixture
    def mocked_testbot(self, testbot, mocked_user_profile):
        config = create_config()
        config['EMAIL_SLACK_FIELD'] = alternative_email_tag
        config['SENDER_EMAIL_OVERRIDE'] = None
        testbot.bot.sender.userid = 'XXX'
        testbot.bot.find_user_profile = MagicMock(return_value=mocked_user_profile)
        return inject_config(testbot, config)

    def test_alternative_email(self, mocked_testbot):
        mocked_testbot.push_message("access to Xxx")
        mocked_testbot.push_message(f"yes {access_request_id}")
        assert "valid request" in mocked_testbot.pop_message()
        assert "access request" in mocked_testbot.pop_message()
        granting_message = mocked_testbot.pop_message()
        assert "Granting" in granting_message
        assert alternative_email in granting_message

class Test_override_email(ErrBotExtraTestSettings):
    override_email = 'override@email.com'

    @pytest.fixture
    def mocked_testbot(self, testbot):
        config = create_config()
        config['SENDER_EMAIL_OVERRIDE'] = self.override_email
        return inject_config(testbot, config)

    def test_override_email(self, mocked_testbot):
        mocked_testbot.push_message("access to Xxx")
        mocked_testbot.push_message(f"yes {access_request_id}")
        assert "valid request" in mocked_testbot.pop_message()
        assert "access request" in mocked_testbot.pop_message()
        granting_message = mocked_testbot.pop_message()
        assert "Granting" in granting_message
        assert self.override_email in granting_message

class Test_email_subaddress(ErrBotExtraTestSettings):
    account_name_with_subaddress = 'myaccount+stable@test.com'
    email_subaddress = 'stable'

    @pytest.fixture
    def mocked_testbot(self, testbot):
        config = create_config()
        config['SENDER_EMAIL_OVERRIDE'] = None
        config['SENDER_NICK_OVERRIDE'] = None
        config['EMAIL_SUBADDRESS'] = self.email_subaddress
        return inject_config(testbot, config, admins=[f'@{account_name}'])

    def test_email_subaddress(self, mocked_testbot):
        mocked_testbot._bot.callback_message = MagicMock(side_effect=callback_message_fn(
            mocked_testbot._bot,
            from_email=account_name,
            from_nick=account_name
        ))
        mocked_testbot.push_message("access to Xxx")
        mocked_testbot.push_message(f"yes {access_request_id}")
        assert "valid request" in mocked_testbot.pop_message()
        assert "access request" in mocked_testbot.pop_message()
        granting_message = mocked_testbot.pop_message()
        assert "Granting" in granting_message
        assert self.account_name_with_subaddress in granting_message

class Test_custom_resource_grant_timeout(ErrBotExtraTestSettings):
    timeout = 1

    @pytest.fixture
    def mocked_testbot(self, testbot):
        config = create_config()
        timeout_grant_tag = 'grant-timeout'
        config['RESOURCE_GRANT_TIMEOUT_TAG'] = timeout_grant_tag
        return inject_config(testbot, config, tags={timeout_grant_tag: f'{self.timeout}'})

    def test_access_command_grant_auto_approved_for_tagged_resource(self, mocked_testbot):
        mocked_testbot.push_message("access to Xxx")
        mocked_testbot.push_message(f'yes {access_request_id}')
        assert "valid request" in mocked_testbot.pop_message()
        assert "access request" in mocked_testbot.pop_message()
        granting_message = mocked_testbot.pop_message()
        assert "Granting" in granting_message
        assert f"{self.timeout} minutes" in granting_message

class Test_change_error_message(ErrBotExtraTestSettings):
    @pytest.fixture
    def mocked_testbot(self, testbot):
        return inject_config(testbot, create_config())

    def test_error_message(self, mocked_testbot):
        accessbot = mocked_testbot.bot.plugin_manager.plugins['AccessBot']
        accessbot.get_sdm_service().get_account_by_email = MagicMock(side_effect=Exception('Something failed'))

        mocked_testbot.push_message("access to Xxx")
        assert "An error occurred" in mocked_testbot.pop_message()

class Test_acknowledgement_message:
    @pytest.fixture
    def mocked_testbot_with_admins_channel(self, testbot):
        config = create_config()
        config['ADMINS_CHANNEL'] = 'channel'
        return inject_config(testbot, config)

    @pytest.fixture
    def mocked_testbot_without_admin_channel(self, testbot):
        config = create_config()
        config['ADMINS_CHANNEL'] = None
        return inject_config(testbot, config)

    def Test_acknowledgement_message_when_admins_channel_is_configured(self, mocked_testbot_with_admins_channel):
        mocked_testbot_with_admins_channel.push_message("access to Xxx")
        acknowledgement_message = mocked_testbot_with_admins_channel.pop_message()
        assert "valid request" in acknowledgement_message
        assert "configured admin channel" in acknowledgement_message

    def Test_acknowledgement_message_when_team_admins_is_configured(self, mocked_testbot_with_admins_channel):
        mocked_testbot_with_admins_channel.push_message("access to Xxx")
        acknowledgement_message = mocked_testbot_with_admins_channel.pop_message()
        assert "valid request" in acknowledgement_message
        assert "team admins" in acknowledgement_message

class Test_approvers_channel_tag(ErrBotExtraTestSettings):
    raw_messages = []
    regular_channel_name = 'regular-channel'
    admins_channel_name = 'admins-channel'
    approvers_channel_name = 'resource-approvers-channel'

    @pytest.fixture
    def mocked_testbot(self, testbot):
        config = create_config()
        config['APPROVERS_CHANNEL_TAG'] = 'approvers-channel'
        testbot.bot.send_message = send_message_override(testbot.bot, self.raw_messages)
        testbot.bot.channels = MagicMock(return_value=[{'name': self.approvers_channel_name, 'is_member': True}])
        bot = inject_config(testbot, config, tags={'approvers-channel': self.approvers_channel_name })
        bot.bot.plugin_manager.plugins['AccessBot'].build_identifier = MagicMock(
            side_effect=mocked_build_identifier
        )
        return bot

    @pytest.fixture
    def mocked_testbot_resource_without_approvers_tag(self, testbot):
        config = create_config()
        config['ADMINS_CHANNEL'] = f"#{self.admins_channel_name}"
        config['APPROVERS_CHANNEL_TAG'] = 'approvers-channel'
        testbot.bot.send_message = send_message_override(testbot.bot, self.raw_messages)
        testbot.bot.channels = MagicMock(return_value=[
            {'name': self.admins_channel_name, 'is_member': True},
            {'name': self.approvers_channel_name, 'is_member': True},
        ])
        bot = inject_config(testbot, config)
        bot.bot.plugin_manager.plugins['AccessBot'].build_identifier = MagicMock(
            side_effect=mocked_build_identifier
        )
        return bot

    @pytest.fixture
    def mocked_testbot_with_wrong_config(self, testbot):
        config = create_config()
        config['APPROVERS_CHANNEL_TAG'] = 'approvers-channel'
        testbot.bot.channels = MagicMock(return_value=[{'name': self.approvers_channel_name, 'is_member': True}])
        return inject_config(testbot, config, tags={'approvers-channel': 'wrong-group'})

    @pytest.fixture
    def mocked_testbot_with_admins_channel(self, testbot):
        config = create_config()
        config['ADMINS_CHANNEL'] = f"#{self.admins_channel_name}"
        config['APPROVERS_CHANNEL_TAG'] = 'approvers-channel'
        testbot.bot.send_message = send_message_override(testbot.bot, self.raw_messages)
        testbot.bot.channels = MagicMock(return_value=[
            {'name': self.admins_channel_name, 'is_member': True},
            {'name': self.approvers_channel_name, 'is_member': True}
        ])
        bot = inject_config(testbot, config, tags={'approvers-channel': self.approvers_channel_name })
        bot.bot.plugin_manager.plugins['AccessBot'].build_identifier = MagicMock(
            side_effect=mocked_build_identifier
        )
        return bot

    def test_access_command_send_request_message_to_respective_channels(self, mocked_testbot):
        mocked_testbot.bot.sender.room = create_room_mock(self.approvers_channel_name)
        mocked_testbot.push_message("access to Xxx")
        mocked_testbot.push_message(f"yes {access_request_id}")
        ack_message = mocked_testbot.pop_message()
        assert "valid request" in ack_message
        assert "configured approvers channel" in ack_message
        assert "access request" in mocked_testbot.pop_message()
        assert "Granting" in mocked_testbot.pop_message()
        assert self.raw_messages[1].to.person == f"#{self.approvers_channel_name}"
        self.raw_messages.clear()

    def test_access_command_send_request_message_to_admins_channel(self, mocked_testbot_resource_without_approvers_tag):
        mocked_testbot_resource_without_approvers_tag.bot.sender.room = create_room_mock(self.admins_channel_name)
        mocked_testbot_resource_without_approvers_tag.push_message("access to Xxx")
        mocked_testbot_resource_without_approvers_tag.push_message(f"yes {access_request_id}")
        ack_message = mocked_testbot_resource_without_approvers_tag.pop_message()
        assert "valid request" in ack_message
        assert "configured admins channel" in ack_message
        assert "access request" in mocked_testbot_resource_without_approvers_tag.pop_message()
        assert "Granting" in mocked_testbot_resource_without_approvers_tag.pop_message()
        assert self.raw_messages[1].to.person == f"#{self.admins_channel_name}"
        self.raw_messages.clear()

    def test_access_command_fails_when_approvers_channel_is_unreachable(self, mocked_testbot_with_wrong_config):
        '''
        This test should raise an Exception when trying to build an identifier for an unreachable channel.
        '''
        mocked_testbot_with_wrong_config.bot.plugin_manager.plugins['AccessBot'].build_identifier = MagicMock(
            side_effect=[
                # build_identifier needs to return a mocked identifier for each admin before throwing the wanted Exception
                get_dummy_person('@sdm_admin'),
                raise_no_identifier
            ]
        )
        mocked_testbot_with_wrong_config.push_message("access to Xxx")
        assert "cannot contact the approvers for this resource, their channel is unreachable" in mocked_testbot_with_wrong_config.pop_message()

    def test_fail_to_approve_access_command_from_admins_channel(self, mocked_testbot_with_admins_channel):
        mocked_testbot_with_admins_channel.push_message("access to Xxx")
        mocked_testbot_with_admins_channel._bot.callback_message = MagicMock(side_effect=callback_message_fn(
            mocked_testbot_with_admins_channel._bot,
            room_name=self.admins_channel_name
        ))
        mocked_testbot_with_admins_channel.push_message(f"yes {access_request_id}")
        ack_message = mocked_testbot_with_admins_channel.pop_message()
        assert "valid request" in ack_message
        assert "configured approvers channel" in ack_message
        assert "access request" in mocked_testbot_with_admins_channel.pop_message()
        assert self.raw_messages[1].to.person == f"#{self.approvers_channel_name}"
        assert "using the wrong channel" in mocked_testbot_with_admins_channel.pop_message()
        self.raw_messages.clear()

    def test_access_command_ignores_unreachable_admins_channel_when_approvers_channel_is_configured(self, mocked_testbot):
        accessbot = mocked_testbot.bot.plugin_manager.plugins['AccessBot']
        accessbot.config['ADMINS_CHANNEL'] = '#unreachable-channel'
        mocked_testbot.push_message("access to Xxx")
        ack_message = mocked_testbot.pop_message()
        assert "valid request" in ack_message
        assert "configured approvers channel" in ack_message
        assert "access request" in mocked_testbot.pop_message()
        assert self.raw_messages[1].to.person == f"#{self.approvers_channel_name}"
        self.raw_messages.clear()

class Test_check_permission(ErrBotExtraTestSettings):
    @pytest.fixture
    def mocked_testbot_account_grant_exists(self, testbot):
        return inject_config(testbot, create_config(), account_grant_exists=True)

    @pytest.fixture
    def mocked_testbot_account_grant_doesnt_exists(self, testbot):
        return inject_config(testbot, create_config())

    def test_when_account_grant_exists(self, mocked_testbot_account_grant_exists):
        accessbot = mocked_testbot_account_grant_exists.bot.plugin_manager.plugins["AccessBot"]
        with pytest.raises(Exception) as ex:
            accessbot.get_resource_grant_helper().check_permission(create_resource_mock(None), create_account_mock(), '')
        assert "already have access" in str(ex.value)

    def test_when_account_grant_doesnt_exists(self, mocked_testbot_account_grant_doesnt_exists):
        accessbot = mocked_testbot_account_grant_doesnt_exists.bot.plugin_manager.plugins["AccessBot"]
        result = accessbot.get_resource_grant_helper().check_permission(create_resource_mock(None), create_account_mock(), '')
        assert not result


class Test_access_request_renewal(ErrBotExtraTestSettings):
    raw_messages = []
    regular_channel_name = 'regular-channel'
    admins_channel_name = 'admins-channel'

    @pytest.fixture
    def mocked_testbot(self, testbot):
        config = create_config()
        testbot.bot.channels = MagicMock(return_value=[
            {'name': self.admins_channel_name, 'is_member': True},
            {'name': self.regular_channel_name, 'is_member': True},
        ])
        config['ADMINS_CHANNEL'] = f'#{self.admins_channel_name}'
        config['ALLOW_RESOURCE_ACCESS_REQUEST_RENEWAL'] = True
        testbot.bot.send_message = send_message_override(testbot.bot, self.raw_messages)
        bot = inject_config(testbot, config, account_grant_exists=True)
        bot.bot.plugin_manager.plugins['AccessBot'].build_identifier = MagicMock(
            side_effect=mocked_build_identifier
        )
        return bot

    def test_access_command_grant_renewal(self, mocked_testbot):
        mocked_testbot._bot.callback_message = MagicMock(side_effect=callback_message_fn(
            mocked_testbot._bot,
            room_name=self.regular_channel_name
        ))
        mocked_testbot.push_message('access to Xxx')
        assert "valid request" in mocked_testbot.pop_message()
        assert "access request" in mocked_testbot.pop_message()
        assert self.raw_messages[1].to.person == f'#{self.admins_channel_name}'
        assert "Approving the request will revoke the previous grant and create a new one" in mocked_testbot.pop_message()
        mocked_testbot._bot.callback_message = MagicMock(side_effect=callback_message_fn(
            mocked_testbot._bot,
            room_name=self.admins_channel_name
        ))
        mocked_testbot.push_message(f'yes {access_request_id}')
        assert "Access renewed" in mocked_testbot.pop_message()
        assert self.raw_messages[3].to.person == f'#{self.regular_channel_name}'
        granted_message = mocked_testbot.pop_message()
        assert "Granting" in granted_message
        accessbot = mocked_testbot.bot.plugin_manager.plugins['AccessBot']
        accessbot.get_sdm_service().delete_account_grant.assert_called_with(resource_id, account_id)

    def test_dont_delete_account_grant_when_flag_is_disabled(self, mocked_testbot):
        accessbot = mocked_testbot.bot.plugin_manager.plugins['AccessBot']
        accessbot.config['ALLOW_RESOURCE_ACCESS_REQUEST_RENEWAL'] = False
        mocked_testbot.push_message('access to Xxx')
        assert "already have access" in mocked_testbot.pop_message()
        accessbot.get_sdm_service().delete_account_grant.assert_not_called()

# pylint: disable=dangerous-default-value
def inject_config(testbot, config, admins=["gbin@localhost"], tags={}, resources_by_role=[], account_grant_exists=False,
                  resources=[], account_tags={}):
    accessbot = testbot.bot.plugin_manager.plugins['AccessBot']
    accessbot.config = config
    # The default implementation is not compatible with the backend identifier.
    # Refer to: https://errbot.readthedocs.io/en/4.1/errbot.backends.test.html#errbot.backends.test.TestPerson
    accessbot.build_identifier = MagicMock(return_value=get_dummy_person(account_name))
    accessbot.get_admins = MagicMock(return_value=admins)
    accessbot.get_api_access_key = MagicMock(return_value="api-access_key")
    accessbot.get_api_secret_key = MagicMock(return_value="c2VjcmV0LWtleQ==")  # valid base64 string
    accessbot.get_sdm_service = MagicMock(
        return_value=create_sdm_service_mock(tags, resources_by_role, account_grant_exists, resources, account_tags))
    accessbot.get_resource_grant_helper = MagicMock(return_value=create_resource_grant_helper(accessbot))
    accessbot.get_approve_helper = MagicMock(return_value=create_approve_helper(accessbot))
    testbot._bot.init_access_form_bot = MagicMock(return_value=None)
    return testbot

def create_resource_grant_helper(accessbot):
    helper = ResourceGrantHelper(accessbot)
    helper.generate_grant_request_id = MagicMock(return_value=access_request_id)
    return helper

def create_approve_helper(accessbot):
    return ApproveHelper(accessbot)

def create_sdm_service_mock(tags, resources_by_role, account_grant_exists, resources, account_tags):
    mock = MagicMock()
    if len(resources) > 0:
        mock.get_resource_by_name = MagicMock(side_effect=raise_no_resource_found)
    else:
        mock.get_resource_by_name = MagicMock(return_value=create_resource_mock(tags))
    mock.get_account_by_email = MagicMock(return_value=create_account_mock(account_tags=account_tags))
    mock.grant_temporary_access = MagicMock()
    mock.get_all_resources_by_role = MagicMock(return_value=resources_by_role)
    mock.account_grant_exists = MagicMock(return_value=account_grant_exists)
    mock.get_all_resources = MagicMock(return_value=resources)
    mock.delete_account_grant = MagicMock(return_value=None)
    return mock

def create_resource_mock(tags):
    mock = MagicMock()
    mock.id = resource_id
    mock.name = resource_name
    mock.tags = tags
    return mock

def create_account_mock(account_email=account_name, account_tags={}):
    mock = MagicMock()
    mock.id = account_id
    mock.name = account_name
    mock.email = account_email
    mock.tags = account_tags
    return mock

def create_approver_mock(account_email=account_name):
    mock = MagicMock()
    mock.email = account_email
    mock.nick = account_email
    return mock

def create_room_mock(channel_name):
    mock = MagicMock()
    mock.name = channel_name
    return mock

def raise_no_resource_found(message='', match=''):
    raise NotFoundException('Sorry, cannot find that resource!')

def raise_no_identifier(_):
    raise NotFoundException('No identifier built.')

def mocked_build_identifier(param):
    return get_dummy_person(param)

def mocked_build_identifier_with_nick(param):
    return DummyPerson(param[1:], nick=param[1:])
