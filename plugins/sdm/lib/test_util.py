# pylint: disable=invalid-name

from unittest.mock import MagicMock
from strongdm import Postgres, Role

from .util import is_hidden_resource, can_auto_approve_by_tag, is_hidden_role

class Test_is_hidden_resource:
    def test_hide_resource_when_tag_true(self):
        config = {'HIDE_RESOURCE_TAG': 'hide-resource'}
        sdm_resource = MagicMock(spec = Postgres)
        sdm_resource.tags = {'hide-resource': 'true'}
        assert is_hidden_resource(config, sdm_resource)

    def test_dont_hide_resource_when_tag_false(self):
        config = {'HIDE_RESOURCE_TAG': 'hide-resource'}
        sdm_resource = MagicMock(spec = Postgres)
        sdm_resource.tags = {'hide-resource': 'false'}
        assert is_hidden_resource(config, sdm_resource) is False

    def test_hide_resource_when_tag_have_no_value(self):
        config = {'HIDE_RESOURCE_TAG': 'hide-resource'}
        sdm_resource = MagicMock(spec = Postgres)
        sdm_resource.tags = {'hide-resource': None}
        assert is_hidden_resource(config, sdm_resource)

    def test_hide_resource_when_tag_have_unexpected_value(self):
        config = {'HIDE_RESOURCE_TAG': 'hide-resource'}
        sdm_resource = MagicMock(spec = Postgres)
        sdm_resource.tags = {'hide-resource': 'not-a-boolean'}
        assert is_hidden_resource(config, sdm_resource)

    def test_dont_hide_resource_when_tag_doesnt_exist(self):
        config = {'HIDE_RESOURCE_TAG': 'another-tag'}
        sdm_resource = MagicMock(spec = Postgres)
        sdm_resource.tags = {'hide-resource': 'true'}
        assert is_hidden_resource(config, sdm_resource) is False

class Test_is_hidden_role:
    def test_hide_role_when_tag_true(self):
        config = {'HIDE_ROLE_TAG': 'hide-role'}
        sdm_role = MagicMock(spec = Role)
        sdm_role.tags = {'hide-role': 'true'}
        assert is_hidden_role(config, sdm_role)

    def test_dont_hide_role_when_tag_false(self):
        config = {'HIDE_ROLE_TAG': 'hide-role'}
        sdm_role = MagicMock(spec = Role)
        sdm_role.tags = {'hide-role': 'false'}
        assert not is_hidden_role(config, sdm_role)

    def test_hide_role_when_tag_has_no_value(self):
        config = {'HIDE_ROLE_TAG': 'hide-role'}
        sdm_role = MagicMock(spec = Role)
        sdm_role.tags = {'hide-role': None}
        assert is_hidden_role(config, sdm_role)

    def test_hide_role_when_tag_has_unexpected_value(self):
        config = {'HIDE_ROLE_TAG': 'hide-role'}
        sdm_role = MagicMock(spec = Role)
        sdm_role.tags = {'hide-role': 'not-a-boolean'}
        assert is_hidden_role(config, sdm_role)

    def test_dont_hide_role_when_tag_doesnt_exist(self):
        config = {'HIDE_ROLE_TAG': 'hide-role'}
        sdm_role = MagicMock(spec = Role)
        sdm_role.tags = {'another-tag': 'true'}
        assert not is_hidden_role(config, sdm_role)

class Test_can_auto_approve_by_tag:
    def test_auto_approve_when_tag_true(self):
        config = {'AUTO_APPROVE_TAG': 'auto-approve'}
        sdm_resource = MagicMock(spec = Postgres)
        sdm_resource.tags = {'auto-approve': 'true'}
        assert can_auto_approve_by_tag(config, sdm_resource, 'AUTO_APPROVE_TAG')

    def test_dont_auto_approve_when_tag_false(self):
        config = {'AUTO_APPROVE_TAG': 'auto-approve'}
        sdm_resource = MagicMock(spec = Postgres)
        sdm_resource.tags = {'auto-approve': 'false'}
        assert can_auto_approve_by_tag(config, sdm_resource, 'AUTO_APPROVE_TAG') is False

    def test_auto_approve_when_tag_have_no_value(self):
        config = {'AUTO_APPROVE_TAG': 'auto-approve'}
        sdm_resource = MagicMock(spec = Postgres)
        sdm_resource.tags = {'auto-approve': None}
        assert can_auto_approve_by_tag(config, sdm_resource, 'AUTO_APPROVE_TAG')

    def test_auto_approve_when_tag_have_unexpected_value(self):
        config = {'AUTO_APPROVE_TAG': 'auto-approve'}
        sdm_resource = MagicMock(spec = Postgres)
        sdm_resource.tags = {'auto-approve': 'not-a-boolean'}
        assert can_auto_approve_by_tag(config, sdm_resource, 'AUTO_APPROVE_TAG')

    def test_dont_auto_approve_when_tag_doesnt_exist(self):
        config = {'AUTO_APPROVE_TAG': 'another-tag'}
        sdm_resource = MagicMock(spec = Postgres)
        sdm_resource.tags = {'auto-approve': 'true'}
        assert can_auto_approve_by_tag(config, sdm_resource, 'AUTO_APPROVE_TAG') is False
