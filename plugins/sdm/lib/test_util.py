# pylint: disable=invalid-name
import sys
from unittest.mock import MagicMock
import pytest
from strongdm import Postgres, Role

sys.path.append('e2e/')

from .util import is_hidden, can_auto_approve_by_tag, HiddenTagEnum, AllowedTagEnum, is_allowed, is_concealed
from test_common import DummyPerson


class Test_is_hidden_resource:
    def test_hide_resource_when_tag_true(self):
        config = {'HIDE_RESOURCE_TAG': 'hide-resource'}
        sdm_resource = MagicMock(spec = Postgres)
        sdm_resource.tags = {'hide-resource': 'true'}
        assert is_hidden(config, HiddenTagEnum.RESOURCE, sdm_resource)

    def test_dont_hide_resource_when_tag_false(self):
        config = {'HIDE_RESOURCE_TAG': 'hide-resource'}
        sdm_resource = MagicMock(spec = Postgres)
        sdm_resource.tags = {'hide-resource': 'false'}
        assert is_hidden(config, HiddenTagEnum.RESOURCE, sdm_resource) is False

    def test_hide_resource_when_tag_have_no_value(self):
        config = {'HIDE_RESOURCE_TAG': 'hide-resource'}
        sdm_resource = MagicMock(spec = Postgres)
        sdm_resource.tags = {'hide-resource': None}
        assert is_hidden(config, HiddenTagEnum.RESOURCE, sdm_resource)

    def test_hide_resource_when_tag_have_unexpected_value(self):
        config = {'HIDE_RESOURCE_TAG': 'hide-resource'}
        sdm_resource = MagicMock(spec = Postgres)
        sdm_resource.tags = {'hide-resource': 'not-a-boolean'}
        assert is_hidden(config, HiddenTagEnum.RESOURCE, sdm_resource)

    def test_dont_hide_resource_when_tag_doesnt_exist(self):
        config = {'HIDE_RESOURCE_TAG': 'another-tag'}
        sdm_resource = MagicMock(spec = Postgres)
        sdm_resource.tags = {'hide-resource': 'true'}
        assert is_hidden(config, HiddenTagEnum.RESOURCE, sdm_resource) is False

class Test_is_allowed_resource:
    def test_allow_resource_when_tag_true(self):
        config = {'ALLOW_RESOURCE_TAG': 'allow-resource'}
        sdm_resource = MagicMock(spec = Postgres)
        sdm_resource.tags = {'allow-resource': 'true'}
        assert is_allowed(config, AllowedTagEnum.RESOURCE, sdm_resource)

    def test_dont_allow_resource_when_tag_false(self):
        config = {'ALLOW_RESOURCE_TAG': 'allow-resource'}
        sdm_resource = MagicMock(spec = Postgres)
        sdm_resource.tags = {'allow-resource': 'false'}
        assert is_allowed(config, AllowedTagEnum.RESOURCE, sdm_resource) is False

    def test_allow_resource_when_tag_have_no_value(self):
        config = {'ALLOW_RESOURCE_TAG': 'allow-resource'}
        sdm_resource = MagicMock(spec = Postgres)
        sdm_resource.tags = {'allow-resource': None}
        assert is_allowed(config, AllowedTagEnum.RESOURCE, sdm_resource)

    def test_allow_resource_when_tag_have_unexpected_value(self):
        config = {'ALLOW_RESOURCE_TAG': 'allow-resource'}
        sdm_resource = MagicMock(spec = Postgres)
        sdm_resource.tags = {'allow-resource': 'not-a-boolean'}
        assert is_allowed(config, AllowedTagEnum.RESOURCE, sdm_resource)

    def test_dont_allow_resource_when_tag_doesnt_exist(self):
        config = {'ALLOW_RESOURCE_TAG': 'another-tag'}
        sdm_resource = MagicMock(spec = Postgres)
        sdm_resource.tags = {'allow-resource': 'true'}
        assert is_allowed(config, AllowedTagEnum.RESOURCE, sdm_resource) is False


class Test_is_concealed_resource:
    def test_conceal_resource_when_tag_true(self):
        config = {'CONCEAL_RESOURCE_TAG': 'conceal-resource'}
        sdm_resource = MagicMock(spec = Postgres)
        sdm_resource.tags = {'conceal-resource': 'true'}
        assert is_concealed(config, sdm_resource)

    def test_dont_conceal_resource_when_tag_false(self):
        config = {'CONCEAL_RESOURCE_TAG': 'conceal-resource'}
        sdm_resource = MagicMock(spec = Postgres)
        sdm_resource.tags = {'conceal-resource': 'false'}
        assert is_concealed(config, sdm_resource) is False

    def test_conceal_resource_when_tag_have_no_value(self):
        config = {'CONCEAL_RESOURCE_TAG': 'conceal-resource'}
        sdm_resource = MagicMock(spec = Postgres)
        sdm_resource.tags = {'conceal-resource': None}
        assert is_concealed(config, sdm_resource)

    def test_conceal_resource_when_tag_have_unexpected_value(self):
        config = {'CONCEAL_RESOURCE_TAG': 'conceal-resource'}
        sdm_resource = MagicMock(spec = Postgres)
        sdm_resource.tags = {'conceal-resource': 'not-a-boolean'}
        assert is_concealed(config, sdm_resource)

    def test_dont_conceal_resource_when_tag_doesnt_exist(self):
        config = {'CONCEAL_RESOURCE_TAG': 'another-tag'}
        sdm_resource = MagicMock(spec = Postgres)
        sdm_resource.tags = {'conceal-resource': 'true'}
        assert is_concealed(config, sdm_resource) is False

class Test_is_hidden_role:
    def test_hide_role_when_tag_true(self):
        config = {'HIDE_ROLE_TAG': 'hide-role'}
        sdm_role = MagicMock(spec = Role)
        sdm_role.tags = {'hide-role': 'true'}
        assert is_hidden(config, HiddenTagEnum.ROLE, sdm_role)

    def test_dont_hide_role_when_tag_false(self):
        config = {'HIDE_ROLE_TAG': 'hide-role'}
        sdm_role = MagicMock(spec = Role)
        sdm_role.tags = {'hide-role': 'false'}
        assert not is_hidden(config, HiddenTagEnum.ROLE, sdm_role)

    def test_hide_role_when_tag_has_no_value(self):
        config = {'HIDE_ROLE_TAG': 'hide-role'}
        sdm_role = MagicMock(spec = Role)
        sdm_role.tags = {'hide-role': None}
        assert is_hidden(config, HiddenTagEnum.ROLE, sdm_role)

    def test_hide_role_when_tag_has_unexpected_value(self):
        config = {'HIDE_ROLE_TAG': 'hide-role'}
        sdm_role = MagicMock(spec = Role)
        sdm_role.tags = {'hide-role': 'not-a-boolean'}
        assert is_hidden(config, HiddenTagEnum.ROLE, sdm_role)

    def test_dont_hide_role_when_tag_doesnt_exist(self):
        config = {'HIDE_ROLE_TAG': 'hide-role'}
        sdm_role = MagicMock(spec = Role)
        sdm_role.tags = {'another-tag': 'true'}
        assert not is_hidden(config, HiddenTagEnum.ROLE, sdm_role)

class Test_can_auto_approve_by_tag:

    @pytest.fixture
    def test_person(self):
        return DummyPerson('@test', tags={'groups': 'test-group'})

    def test_auto_approve_when_tag_true(self, test_person):
        config = {'AUTO_APPROVE_TAG': 'auto-approve', 'GROUPS_TAG': 'groups'}
        sdm_resource = MagicMock(spec = Postgres)
        sdm_resource.tags = {'auto-approve': 'true'}
        assert can_auto_approve_by_tag(config, sdm_resource, 'AUTO_APPROVE_TAG', test_person)

    def test_dont_auto_approve_when_tag_false(self, test_person):
        config = {'AUTO_APPROVE_TAG': 'auto-approve', 'GROUPS_TAG': 'groups'}
        sdm_resource = MagicMock(spec = Postgres)
        sdm_resource.tags = {'auto-approve': 'false'}
        assert can_auto_approve_by_tag(config, sdm_resource, 'AUTO_APPROVE_TAG', test_person) is False

    def test_auto_approve_when_tag_have_no_value(self, test_person):
        config = {'AUTO_APPROVE_TAG': 'auto-approve', 'GROUPS_TAG': 'groups'}
        sdm_resource = MagicMock(spec = Postgres)
        sdm_resource.tags = {'auto-approve': None}
        assert can_auto_approve_by_tag(config, sdm_resource, 'AUTO_APPROVE_TAG', test_person)

    def test_dont_auto_approve_when_tag_doesnt_exist(self, test_person):
        config = {'AUTO_APPROVE_TAG': 'another-tag', 'GROUPS_TAG': 'groups'}
        sdm_resource = MagicMock(spec = Postgres)
        sdm_resource.tags = {'auto-approve': 'true'}
        assert can_auto_approve_by_tag(config, sdm_resource, 'AUTO_APPROVE_TAG', test_person) is False
