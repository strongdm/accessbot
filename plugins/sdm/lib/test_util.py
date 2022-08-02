# pylint: disable=invalid-name
from datetime import timedelta
from unittest.mock import MagicMock

import sys
import pytest
from strongdm import Postgres, Role

sys.path.append('e2e/')

from test_common import DummyAccount, DummyResource
from .util import is_hidden, can_auto_approve_by_tag, HiddenTagEnum, AllowedTagEnum, is_allowed, is_concealed, \
    can_auto_approve_by_groups_tag, has_intersection, convert_duration_flag_to_timedelta, \
    get_formatted_duration_string, get_approvers_channel, AllowedGroupsTagEnum


default_group = 'a-group'

class Test_is_hidden_resource:

    @pytest.fixture
    def mocked_resource(self):
        return MagicMock(spec = Postgres)

    def test_hide_resource_when_tag_true(self, mocked_resource):
        config = {'HIDE_RESOURCE_TAG': 'hide-resource'}
        mocked_resource.tags = {'hide-resource': 'true'}
        assert is_hidden(config, HiddenTagEnum.RESOURCE, mocked_resource)

    def test_dont_hide_resource_when_tag_false(self, mocked_resource):
        config = {'HIDE_RESOURCE_TAG': 'hide-resource'}
        mocked_resource.tags = {'hide-resource': 'false'}
        assert not is_hidden(config, HiddenTagEnum.RESOURCE, mocked_resource)

    def test_hide_resource_when_tag_have_no_value(self, mocked_resource):
        config = {'HIDE_RESOURCE_TAG': 'hide-resource'}
        mocked_resource.tags = {'hide-resource': None}
        assert is_hidden(config, HiddenTagEnum.RESOURCE, mocked_resource)

    def test_hide_resource_when_tag_have_unexpected_value(self, mocked_resource):
        config = {'HIDE_RESOURCE_TAG': 'hide-resource'}
        mocked_resource.tags = {'hide-resource': 'not-a-boolean'}
        assert is_hidden(config, HiddenTagEnum.RESOURCE, mocked_resource)

    def test_dont_hide_resource_when_tag_doesnt_exist(self, mocked_resource):
        config = {'HIDE_RESOURCE_TAG': 'another-tag'}
        mocked_resource.tags = {'hide-resource': 'true'}
        assert not is_hidden(config, HiddenTagEnum.RESOURCE, mocked_resource)

class Test_is_allowed_resource:

    @pytest.fixture
    def mocked_resource(self):
        return MagicMock(spec = Postgres)

    @pytest.fixture
    def mocked_account(self):
        return DummyAccount('gbin', {})

    def test_allow_resource_when_tag_true(self, mocked_account):
        config = {'ALLOW_RESOURCE_TAG': 'allow-resource'}
        mocked_resource = MagicMock(spec = Postgres)
        mocked_resource.tags = {'allow-resource': 'true'}
        assert is_allowed(config, AllowedTagEnum.RESOURCE, AllowedGroupsTagEnum.RESOURCE, mocked_resource, mocked_account)

    def test_dont_allow_resource_when_tag_false(self, mocked_resource, mocked_account):
        config = {'ALLOW_RESOURCE_TAG': 'allow-resource'}
        mocked_resource.tags = {'allow-resource': 'false'}
        assert not is_allowed(config, AllowedTagEnum.RESOURCE, AllowedGroupsTagEnum.RESOURCE, mocked_resource, mocked_account)

    def test_allow_resource_when_tag_have_no_value(self, mocked_resource, mocked_account):
        config = {'ALLOW_RESOURCE_TAG': 'allow-resource'}
        mocked_resource.tags = {'allow-resource': None}
        assert is_allowed(config, AllowedTagEnum.RESOURCE, AllowedGroupsTagEnum.RESOURCE, mocked_resource, mocked_account)

    def test_allow_resource_when_tag_have_unexpected_value(self, mocked_resource, mocked_account):
        config = {'ALLOW_RESOURCE_TAG': 'allow-resource'}
        mocked_resource.tags = {'allow-resource': 'not-a-boolean'}
        assert is_allowed(config, AllowedTagEnum.RESOURCE, AllowedGroupsTagEnum.RESOURCE, mocked_resource, mocked_account)

    def test_dont_allow_resource_when_tag_doesnt_exist(self, mocked_resource, mocked_account):
        config = {'ALLOW_RESOURCE_TAG': 'another-tag'}
        mocked_resource.tags = {'allow-resource': 'true'}
        assert not is_allowed(config, AllowedTagEnum.RESOURCE, AllowedGroupsTagEnum.RESOURCE, mocked_resource, mocked_account)

    def test_allow_resource_when_groups_tag_match(self, mocked_resource, mocked_account):
        config = {'GROUPS_TAG': 'groups', 'ALLOW_RESOURCE_GROUPS_TAG': 'allow-groups'}
        mocked_resource.tags = {'allow-groups': f'other-group,{default_group}'}
        mocked_account.tags = {'groups': default_group}
        assert is_allowed(config, AllowedTagEnum.RESOURCE, AllowedGroupsTagEnum.RESOURCE, mocked_resource, mocked_account)

    def test_dont_allow_resource_when_groups_tag_dont_match(self, mocked_resource, mocked_account):
        config = {'GROUPS_TAG': 'groups', 'ALLOW_RESOURCE_GROUPS_TAG': 'allow-groups'}
        mocked_resource.tags = {'allow-groups': 'other-group'}
        mocked_account.tags = {'groups': default_group}
        assert not is_allowed(config, AllowedTagEnum.RESOURCE, AllowedGroupsTagEnum.RESOURCE, mocked_resource, mocked_account)

    def test_allow_resource_when_allow_tag_is_false_and_groups_tag_match(self, mocked_resource, mocked_account):
        config = {'GROUPS_TAG': 'groups', 'ALLOW_RESOURCE_GROUPS_TAG': 'allow-groups', 'ALLOW_RESOURCE_TAG': 'allow-resource'}
        mocked_resource.tags = {'allow-resource': 'false', 'allow-groups': f'other-group,{default_group}'}
        mocked_account.tags = {'groups': default_group}
        assert is_allowed(config, AllowedTagEnum.RESOURCE, AllowedGroupsTagEnum.RESOURCE, mocked_resource, mocked_account)

    def test_allow_resource_when_allow_tag_is_true_and_groups_tag_dont_match(self, mocked_resource, mocked_account):
        config = {'GROUPS_TAG': 'groups', 'ALLOW_RESOURCE_GROUPS_TAG': 'allow-groups', 'ALLOW_RESOURCE_TAG': 'allow-resource'}
        mocked_resource.tags = {'allow-resource': 'true', 'allow-groups': f'other-group'}
        mocked_account.tags = {'groups': default_group}
        assert is_allowed(config, AllowedTagEnum.RESOURCE, AllowedGroupsTagEnum.RESOURCE, mocked_resource, mocked_account)

    def test_allow_resource_when_all_allow_tags_enabled(self, mocked_resource, mocked_account):
        config = {'GROUPS_TAG': 'groups', 'ALLOW_RESOURCE_GROUPS_TAG': 'allow-groups', 'ALLOW_RESOURCE_TAG': 'allow-resource'}
        mocked_resource.tags = {'allow-resource': 'true', 'allow-groups': f'other-group,{default_group}'}
        mocked_account.tags = {'groups': default_group}
        assert is_allowed(config, AllowedTagEnum.RESOURCE, AllowedGroupsTagEnum.RESOURCE, mocked_resource, mocked_account)

    def test_dont_allow_resource_when_all_allow_tags_enabled_and_doesnt_match(self, mocked_resource, mocked_account):
        config = {'GROUPS_TAG': 'groups', 'ALLOW_RESOURCE_GROUPS_TAG': 'allow-groups', 'ALLOW_RESOURCE_TAG': 'allow-resource'}
        mocked_resource.tags = {'allow-resource': 'false', 'allow-groups': f'other-group'}
        mocked_account.tags = {'groups': default_group}
        assert not is_allowed(config, AllowedTagEnum.RESOURCE, AllowedGroupsTagEnum.RESOURCE, mocked_resource, mocked_account)

class Test_is_concealed_resource:

    @pytest.fixture
    def mocked_resource(self):
        return MagicMock(spec=Postgres)

    @pytest.fixture
    def mocked_account(self):
        return DummyAccount('gbin', {})

    def test_conceal_resource_when_tag_true(self, mocked_resource):
        config = {'CONCEAL_RESOURCE_TAG': 'conceal-resource'}
        mocked_resource.tags = {'conceal-resource': 'true'}
        assert is_concealed(config, mocked_resource)

    def test_dont_conceal_resource_when_tag_false(self, mocked_resource):
        config = {'CONCEAL_RESOURCE_TAG': 'conceal-resource'}
        mocked_resource.tags = {'conceal-resource': 'false'}
        assert not is_concealed(config, mocked_resource)

    def test_conceal_resource_when_tag_have_no_value(self, mocked_resource):
        config = {'CONCEAL_RESOURCE_TAG': 'conceal-resource'}
        mocked_resource.tags = {'conceal-resource': None}
        assert is_concealed(config, mocked_resource)

    def test_conceal_resource_when_tag_have_unexpected_value(self, mocked_resource):
        config = {'CONCEAL_RESOURCE_TAG': 'conceal-resource'}
        mocked_resource.tags = {'conceal-resource': 'not-a-boolean'}
        assert is_concealed(config, mocked_resource)

    def test_dont_conceal_resource_when_tag_doesnt_exist(self, mocked_resource):
        config = {'CONCEAL_RESOURCE_TAG': 'another-tag'}
        mocked_resource.tags = {'conceal-resource': 'true'}
        assert not is_concealed(config, mocked_resource)

    def test_dont_allow_resource_when_groups_tag_dont_match(self, mocked_resource, mocked_account):
        config = {'GROUPS_TAG': 'groups', 'ALLOW_RESOURCE_GROUPS_TAG': 'allow-groups'}
        mocked_resource.tags = {'allow-groups': 'other-group'}
        mocked_account.tags = {'groups': default_group}
        assert not is_allowed(config, AllowedTagEnum.RESOURCE, AllowedGroupsTagEnum.RESOURCE, mocked_resource, mocked_account)

    def test_allow_resource_when_allow_tag_is_false_and_groups_tag_match(self, mocked_resource, mocked_account):
        config = {'GROUPS_TAG': 'groups', 'ALLOW_RESOURCE_GROUPS_TAG': 'allow-groups', 'ALLOW_RESOURCE_TAG': 'allow-resource'}
        mocked_resource.tags = {'allow-resource': 'false', 'allow-groups': f'other-group,{default_group}'}
        mocked_account.tags = {'groups': default_group}
        assert is_allowed(config, AllowedTagEnum.RESOURCE, AllowedGroupsTagEnum.RESOURCE, mocked_resource, mocked_account)

    def test_allow_resource_when_allow_tag_is_true_and_groups_tag_dont_match(self, mocked_resource, mocked_account):
        config = {'GROUPS_TAG': 'groups', 'ALLOW_RESOURCE_GROUPS_TAG': 'allow-groups', 'ALLOW_RESOURCE_TAG': 'allow-resource'}
        mocked_resource.tags = {'allow-resource': 'true', 'allow-groups': f'other-group'}
        mocked_account.tags = {'groups': default_group}
        assert is_allowed(config, AllowedTagEnum.RESOURCE, AllowedGroupsTagEnum.RESOURCE, mocked_resource, mocked_account)

    def test_allow_resource_when_all_allow_tags_enabled(self, mocked_resource, mocked_account):
        config = {'GROUPS_TAG': 'groups', 'ALLOW_RESOURCE_GROUPS_TAG': 'allow-groups', 'ALLOW_RESOURCE_TAG': 'allow-resource'}
        mocked_resource.tags = {'allow-resource': 'true', 'allow-groups': f'other-group,{default_group}'}
        mocked_account.tags = {'groups': default_group}
        assert is_allowed(config, AllowedTagEnum.RESOURCE, AllowedGroupsTagEnum.RESOURCE, mocked_resource, mocked_account)

    def test_dont_allow_resource_when_all_allow_tags_enabled_and_doesnt_match(self, mocked_resource, mocked_account):
        config = {'GROUPS_TAG': 'groups', 'ALLOW_RESOURCE_GROUPS_TAG': 'allow-groups', 'ALLOW_RESOURCE_TAG': 'allow-resource'}
        mocked_resource.tags = {'allow-resource': 'false', 'allow-groups': f'other-group'}
        mocked_account.tags = {'groups': default_group}
        assert not is_allowed(config, AllowedTagEnum.RESOURCE, AllowedGroupsTagEnum.RESOURCE, mocked_resource, mocked_account)

class Test_is_hidden_role:

    @pytest.fixture
    def mocked_role(self):
        return MagicMock(spec=Role)

    def test_hide_role_when_tag_true(self, mocked_role):
        config = {'HIDE_ROLE_TAG': 'hide-role'}
        mocked_role.tags = {'hide-role': 'true'}
        assert is_hidden(config, HiddenTagEnum.ROLE, mocked_role)

    def test_dont_hide_role_when_tag_false(self, mocked_role):
        config = {'HIDE_ROLE_TAG': 'hide-role'}
        mocked_role.tags = {'hide-role': 'false'}
        assert not is_hidden(config, HiddenTagEnum.ROLE, mocked_role)

    def test_hide_role_when_tag_has_no_value(self, mocked_role):
        config = {'HIDE_ROLE_TAG': 'hide-role'}
        mocked_role.tags = {'hide-role': None}
        assert is_hidden(config, HiddenTagEnum.ROLE, mocked_role)

    def test_hide_role_when_tag_has_unexpected_value(self, mocked_role):
        config = {'HIDE_ROLE_TAG': 'hide-role'}
        mocked_role.tags = {'hide-role': 'not-a-boolean'}
        assert is_hidden(config, HiddenTagEnum.ROLE, mocked_role)

    def test_dont_hide_role_when_tag_doesnt_exist(self, mocked_role):
        config = {'HIDE_ROLE_TAG': 'hide-role'}
        mocked_role.tags = {'another-tag': 'true'}
        assert not is_hidden(config, HiddenTagEnum.ROLE, mocked_role)

class Test_is_allowed_role:

    @pytest.fixture
    def mocked_role(self):
        return MagicMock(spec = Role)

    @pytest.fixture
    def mocked_account(self):
        return DummyAccount('gbin', {})

    def test_allow_role_when_tag_true(self, mocked_role, mocked_account):
        config = {'ALLOW_ROLE_TAG': 'allow-role'}
        mocked_role.tags = {'allow-role': 'true'}
        assert is_allowed(config, AllowedTagEnum.ROLE, AllowedGroupsTagEnum.ROLE, mocked_role, mocked_account)

    def test_dont_allow_role_when_tag_false(self, mocked_role, mocked_account):
        config = {'ALLOW_ROLE_TAG': 'allow-role'}
        mocked_role.tags = {'allow-role': 'false'}
        assert not is_allowed(config, AllowedTagEnum.ROLE, AllowedGroupsTagEnum.ROLE, mocked_role, mocked_account)

    def test_allow_role_when_tag_have_no_value(self, mocked_role, mocked_account):
        config = {'ALLOW_ROLE_TAG': 'allow-role'}
        mocked_role.tags = {'allow-role': None}
        assert is_allowed(config, AllowedTagEnum.ROLE, AllowedGroupsTagEnum.ROLE, mocked_role, mocked_account)

    def test_dont_allow_role_when_tag_have_unexpected_value(self, mocked_role, mocked_account):
        config = {'ALLOW_ROLE_TAG': 'allow-role'}
        mocked_role.tags = {'allow-role' : 'not-a-boolean'}
        assert is_allowed(config, AllowedTagEnum.ROLE, AllowedGroupsTagEnum.ROLE, mocked_role, mocked_account)

    def test_dont_allow_role_when_tag_doesnt_exist(self, mocked_role, mocked_account):
        config = {'ALLOW_ROLE_TAG': 'another-tag'}
        mocked_role.tags = {'allow-role': 'true'}
        assert not is_allowed(config, AllowedTagEnum.ROLE, AllowedGroupsTagEnum.ROLE, mocked_role, mocked_account)

    def test_dont_allow_role_when_groups_tag_dont_match(self, mocked_role, mocked_account):
        config = {'GROUPS_TAG': 'groups', 'ALLOW_ROLE_GROUPS_TAG': 'allow-groups'}
        mocked_role.tags = {'allow-groups': 'other-group'}
        mocked_account.tags = {'groups': default_group}
        assert not is_allowed(config, AllowedTagEnum.ROLE, AllowedGroupsTagEnum.ROLE, mocked_role, mocked_account)

    def test_allow_role_when_allow_tag_is_false_and_groups_tag_match(self, mocked_role, mocked_account):
        config = {'GROUPS_TAG': 'groups', 'ALLOW_ROLE_GROUPS_TAG': 'allow-groups', 'ALLOW_ROLE_TAG': 'allow-role'}
        mocked_role.tags = {'allow-role': 'false', 'allow-groups': f'other-group,{default_group}'}
        mocked_account.tags = {'groups': default_group}
        assert is_allowed(config, AllowedTagEnum.ROLE, AllowedGroupsTagEnum.ROLE, mocked_role, mocked_account)

    def test_allow_role_when_allow_tag_is_true_and_groups_tag_dont_match(self, mocked_role, mocked_account):
        config = {'GROUPS_TAG': 'groups', 'ALLOW_ROLE_GROUPS_TAG': 'allow-groups', 'ALLOW_ROLE_TAG': 'allow-role'}
        mocked_role.tags = {'allow-role': 'true', 'allow-groups': f'other-group'}
        mocked_account.tags = {'groups': default_group}
        assert is_allowed(config, AllowedTagEnum.ROLE, AllowedGroupsTagEnum.ROLE, mocked_role, mocked_account)

    def test_allow_role_when_all_allow_tags_enabled(self, mocked_role, mocked_account):
        config = {'GROUPS_TAG': 'groups', 'ALLOW_ROLE_GROUPS_TAG': 'allow-groups', 'ALLOW_ROLE_TAG': 'allow-role'}
        mocked_role.tags = {'allow-role': 'true', 'allow-groups': f'other-group,{default_group}'}
        mocked_account.tags = {'groups': default_group}
        assert is_allowed(config, AllowedTagEnum.ROLE, AllowedGroupsTagEnum.ROLE, mocked_role, mocked_account)

    def test_dont_allow_role_when_all_allow_tags_enabled_and_doesnt_match(self, mocked_role, mocked_account):
        config = {'GROUPS_TAG': 'groups', 'ALLOW_ROLE_GROUPS_TAG': 'allow-groups', 'ALLOW_ROLE_TAG': 'allow-role'}
        mocked_role.tags = {'allow-role': 'false', 'allow-groups': f'other-group'}
        mocked_account.tags = {'groups': default_group}
        assert not is_allowed(config, AllowedTagEnum.ROLE, AllowedGroupsTagEnum.ROLE, mocked_role, mocked_account)

class Test_can_auto_approve_by_tag:

    @pytest.fixture
    def mocked_resource(self):
        return MagicMock(spec=Postgres)

    def test_auto_approve_when_tag_true(self, mocked_resource):
        config = {'AUTO_APPROVE_TAG': 'auto-approve'}
        mocked_resource.tags = {'auto-approve': 'true'}
        assert can_auto_approve_by_tag(config, mocked_resource, 'AUTO_APPROVE_TAG')

    def test_dont_auto_approve_when_tag_false(self, mocked_resource):
        config = {'AUTO_APPROVE_TAG': 'auto-approve'}
        mocked_resource.tags = {'auto-approve': 'false'}
        assert not can_auto_approve_by_tag(config, mocked_resource, 'AUTO_APPROVE_TAG')

    def test_auto_approve_when_tag_have_no_value(self, mocked_resource):
        config = {'AUTO_APPROVE_TAG': 'auto-approve'}
        mocked_resource.tags = {'auto-approve': None}
        assert can_auto_approve_by_tag(config, mocked_resource, 'AUTO_APPROVE_TAG')

    def test_auto_approve_when_tag_have_unexpected_value(self, mocked_resource):
        config = {'AUTO_APPROVE_TAG': 'auto-approve'}
        mocked_resource.tags = {'auto-approve': 'not-a-boolean'}
        assert can_auto_approve_by_tag(config, mocked_resource, 'AUTO_APPROVE_TAG')

    def test_dont_auto_approve_when_tag_doesnt_exist(self, mocked_resource):
        config = {'AUTO_APPROVE_TAG': 'another-tag'}
        mocked_resource.tags = {'auto-approve': 'true'}
        assert not can_auto_approve_by_tag(config, mocked_resource, 'AUTO_APPROVE_TAG')

class Test_can_auto_approve_by_groups_tag:

    @pytest.fixture
    def test_account(self):
        return DummyAccount('test', tags={ 'groups': 'group-a,group-b' })

    @pytest.fixture
    def test_account_without_groups(self):
        return DummyAccount('test', tags={})

    @pytest.fixture
    def mocked_resource(self):
        return MagicMock(spec=Postgres)

    def test_auto_approve_when_has_group_intersection(self, test_account, mocked_resource):
        config = {'AUTO_APPROVE_GROUPS_TAG': 'auto-approve-groups', 'GROUPS_TAG': 'groups'}
        mocked_resource.tags = {'auto-approve-groups': 'group-c,group-a'}
        assert can_auto_approve_by_groups_tag(config, mocked_resource, test_account)

    def test_dont_auto_approve_when_has_no_group_intersection(self, test_account, mocked_resource):
        config = {'AUTO_APPROVE_GROUPS_TAG': 'auto-approve-groups', 'GROUPS_TAG': 'groups'}
        mocked_resource.tags = {'auto-approve-groups': 'group-c'}
        assert can_auto_approve_by_groups_tag(config, mocked_resource, test_account) is False

    def test_dont_auto_approve_when_tag_is_none(self, test_account, mocked_resource):
        config = {'AUTO_APPROVE_GROUPS_TAG': 'auto-approve-groups', 'GROUPS_TAG': 'groups'}
        mocked_resource.tags = {'auto-approve-groups': None}
        assert can_auto_approve_by_groups_tag(config, mocked_resource, test_account) is False

    def test_dont_auto_approve_when_tag_is_empty(self, test_account, mocked_resource):
        config = {'AUTO_APPROVE_GROUPS_TAG': 'auto-approve-groups', 'GROUPS_TAG': 'groups'}
        mocked_resource.tags = {'auto-approve-groups': ''}
        assert can_auto_approve_by_groups_tag(config, mocked_resource, test_account) is False

    def test_dont_auto_approve_when_account_has_no_groups(self, test_account_without_groups, mocked_resource):
        config = {'AUTO_APPROVE_GROUPS_TAG': 'auto-approve-groups', 'GROUPS_TAG': 'groups'}
        mocked_resource.tags = {'auto-approve-groups': 'group-a'}
        assert can_auto_approve_by_groups_tag(config, mocked_resource, test_account_without_groups) is False

class Test_has_intersection:
    def test_has_intersection(self):
        list_a = [1, 2]
        list_b = [2, 3]
        assert has_intersection(list_a, list_b)

    def test_dont_has_intersection(self):
        list_a = [1, 2]
        list_b = [3, 4]
        assert has_intersection(list_a, list_b) is False

    def test_dont_has_intersection_when_empty_list(self):
        list_a = [1, 2]
        list_b = []
        assert has_intersection(list_a, list_b) is False

    def test_dont_has_intersection_when_empty_lists(self):
        list_a = []
        list_b = []
        assert has_intersection(list_a, list_b) is False

class Test_convert_duration_flag_to_timedelta:
    def test_convert_without_time_unit(self):
        duration_flag_value = '50'
        converted_timedelta = convert_duration_flag_to_timedelta(duration_flag_value)
        converted_minutes = converted_timedelta.seconds / 60
        assert converted_minutes == 50

    def test_convert_with_minutes(self):
        duration_flag_value = '50m'
        converted_timedelta = convert_duration_flag_to_timedelta(duration_flag_value)
        converted_minutes = converted_timedelta.seconds / 60
        assert converted_minutes == 50

    def test_convert_with_hours(self):
        duration_flag_value = '17h'
        converted_timedelta = convert_duration_flag_to_timedelta(duration_flag_value)
        converted_hours = converted_timedelta.seconds / (60 * 60)
        assert converted_hours == 17

    def test_convert_with_days(self):
        duration_flag_value = "3d"
        converted_timedelta = convert_duration_flag_to_timedelta(duration_flag_value)
        assert converted_timedelta.days == 3

    def test_convert_with_weeks(self):
        duration_flag_value = '3w'
        converted_timedelta = convert_duration_flag_to_timedelta(duration_flag_value)
        converted_weeks = converted_timedelta.days / 7
        assert converted_weeks == 3

    def test_convert_between_different_units(self):
        duration_flag_value = '48h'
        converted_timedelta = convert_duration_flag_to_timedelta(duration_flag_value)
        assert converted_timedelta.days == 2

class Test_get_formatted_duration_string:
    def test_format_with_minutes(self):
        timedelta_obj = timedelta(minutes=30)
        formatted_str = get_formatted_duration_string(timedelta_obj)
        assert formatted_str == '30 minutes'

    def test_format_with_hours(self):
        timedelta_obj = timedelta(hours=3)
        formatted_str = get_formatted_duration_string(timedelta_obj)
        assert formatted_str == '3 hours'

    def test_format_with_days(self):
        timedelta_obj = timedelta(days=5)
        formatted_str = get_formatted_duration_string(timedelta_obj)
        assert formatted_str == '5 days'

    def test_format_with_weeks(self):
        timedelta_obj = timedelta(weeks=5)
        formatted_str = get_formatted_duration_string(timedelta_obj)
        assert formatted_str == '5 weeks'

    def test_format_with_different_units(self):
        timedelta_obj = timedelta(minutes=120)
        formatted_str = get_formatted_duration_string(timedelta_obj)
        assert formatted_str == '2 hours'

    def test_format_with_multiple_units(self):
        timedelta_obj = timedelta(minutes=90)
        formatted_str = get_formatted_duration_string(timedelta_obj)
        assert formatted_str == '1 hours 30 minutes'

class Test_get_approvers_channel:
    approvers_channel_tag = 'approvers-channel'
    approvers_channel = 'my-channel'

    def test_get_channel_when_flag_is_enable_and_sdm_object_has_tag(self):
        config = {'APPROVERS_CHANNEL_TAG': self.approvers_channel_tag}
        sdm_object = DummyResource('resource', {self.approvers_channel_tag: self.approvers_channel})
        approvers_channel = get_approvers_channel(config, sdm_object)
        assert approvers_channel == self.approvers_channel

    def test_dont_get_channel_when_sdm_object_has_tag_but_flag_is_disabled(self):
        config = {'APPROVERS_CHANNEL_TAG': None}
        sdm_object = DummyResource('resource', {self.approvers_channel_tag: self.approvers_channel})
        approvers_channel = get_approvers_channel(config, sdm_object)
        assert approvers_channel is None

    def test_dont_get_channel_when_flag_is_enabled_but_sdm_object_doesnt_have_tag(self):
        config = {'APPROVERS_CHANNEL_TAG': self.approvers_channel_tag}
        sdm_object = DummyResource('resource', {})
        approvers_channel = get_approvers_channel(config, sdm_object)
        assert approvers_channel is None

    def test_dont_get_channel_when_flag_is_disabled_and_sdm_object_doesnt_have_tag(self):
        config = {'APPROVERS_CHANNEL_TAG': None}
        sdm_object = DummyResource('resource', {})
        approvers_channel = get_approvers_channel(config, sdm_object)
        assert approvers_channel is None
