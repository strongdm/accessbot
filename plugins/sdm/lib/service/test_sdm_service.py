# pylint: disable=redefined-outer-name
# pylint: disable=invalid-name
import datetime
import traceback
from datetime import timezone, timedelta
from unittest.mock import MagicMock, call
import pytest
import strongdm
import sys

from .sdm_service import SdmService

sys.path.append('e2e/')

from test_common import DummyAccountGrant

resource_id = 1
resource_name = "resource1"
role_id = 111
role_name = "role111"
account_id = 55
account_email = "myaccount@test.com"
grant_id = 11
grant_start_from = datetime.datetime.now(timezone.utc) + timedelta(minutes=1)
grant_valid_until = grant_start_from + timedelta(hours=1)

@pytest.fixture()
def client():
    return MagicMock()

@pytest.fixture()
def service(client):
    return SdmService(client, MagicMock())

class Test_get_resource_by_name:
    def test_when_resource_exists_returns_resource(self, client, service):
        client.resources.list = MagicMock(return_value = get_resource_list_iter())
        sdm_resource = service.get_resource_by_name(resource_name)
        assert sdm_resource.id == resource_id
        assert sdm_resource.name == resource_name

    def test_when_sdm_client_fails_raises_exception(self, client, service):
        error_message = "SDM Client failed"
        client.resources.list = MagicMock(side_effect = Exception(error_message))
        with pytest.raises(Exception) as ex:
            service.get_resource_by_name(resource_name)
        assert error_message in str(ex.value)

    def test_when_resource_doesnt_exist_raises_exception(self, client, service):
        client.resources.list = MagicMock(return_value = iter([]))
        with pytest.raises(Exception):
            service.get_resource_by_name(resource_name)

class Test_get_account_by_email:
    def test_when_account_exists_returns_account(self, client, service):
        client.accounts.list = MagicMock(return_value = self.get_account_list_iter())
        sdm_account = service.get_account_by_email(account_email)
        assert sdm_account.id == account_id
        assert sdm_account.email == account_email

    def test_when_sdm_client_fails_raises_exception(self, client, service):
        error_message = "SDM Client failed"
        client.accounts.list = MagicMock(side_effect = Exception(error_message))
        with pytest.raises(Exception) as ex:
            service.get_account_by_email(account_email)
        assert error_message in str(ex.value)

    def test_when_account_doesnt_exist_raises_exception(self, client, service):
        client.accounts.list = MagicMock(return_value = iter([]))
        with pytest.raises(Exception):
            service.get_account_by_email(account_email)

    @staticmethod
    def get_account_list_iter():
        mock_account = MagicMock()
        mock_account.id = account_id
        mock_account.email = account_email
        return iter([mock_account])

class Test_account_grant_exists:
    def test_when_grant_exists(self, client, service):
        client.account_grants.list = MagicMock(return_value=iter(["one resource"]))
        grant_exists = service.account_grant_exists(get_resource(), account_id)
        client.account_grants.list.assert_called_with(f"resource_id:{resource_id},account_id:{account_id}")
        assert grant_exists is True

    def test_when_grant_doesnt_exists(self, client, service):
        client.account_grants.list = MagicMock(return_value=iter([]))
        grant_exists = service.account_grant_exists(get_resource(), account_id)
        client.account_grants.list.assert_called_with(f"resource_id:{resource_id},account_id:{account_id}")
        assert grant_exists is False

    def test_when_grant_exists_fail(self, client, service):
        error_message = "Account grant list failed"
        client.account_grants.list = MagicMock(side_effect = Exception(error_message))
        with pytest.raises(Exception) as ex:
            service.account_grant_exists(get_resource(), account_id)
        assert error_message in str(ex.value)

class Test_delete_account_grant:
    def test_when_grant_exists(self, client, service):
        client.account_grants.list = MagicMock(return_value=[DummyAccountGrant(grant_id)])
        client.account_grants.delete = MagicMock(return_value=None)
        service.delete_account_grant(resource_id, account_id)
        client.account_grants.delete.assert_called_with(grant_id)

    def test_when_grant_doesnt_exists(self, client, service):
        client.account_grants.list = MagicMock(return_value=[])
        client.account_grants.delete = MagicMock(return_value=None)
        service.delete_account_grant(resource_id, account_id)
        client.account_grants.delete.assert_not_called()

    def test_when_grant_list_fails(self, client, service):
        error_message = "Account grant list failed"
        client.account_grants.list = MagicMock(side_effect=Exception(error_message))
        with pytest.raises(Exception) as ex:
            service.delete_account_grant(resource_id, account_id)
        assert error_message in str(ex.value)

    def test_when_grant_delete_fails(self, client, service):
        error_message = "Delete account grant failed"
        client.account_grants.list = MagicMock(return_value=iter([DummyAccountGrant(grant_id)]))
        client.account_grants.delete = MagicMock(side_effect=Exception(error_message))
        with pytest.raises(Exception) as ex:
            service.delete_account_grant(resource_id, account_id)
        assert error_message in str(ex.value)

class Test_role_grant_exists:
    def test_when_grant_exists_using_access_rules(self, client, service):
        client.account_attachments.list = MagicMock(return_value=get_account_attachments())
        client.roles.get = MagicMock(return_value=get_role_response(access_rules=[{'ids': [resource_id]}]))
        client.roles.list = MagicMock(return_value=[get_role()])
        client.role_grants.list = MagicMock(return_value=[get_role_grant()])
        client.resources.list = MagicMock(return_value=get_resource_list_iter())
        grant_exists = service.get_granted_resources_via_role([get_resource()], account_id)
        client.account_attachments.list.assert_called_with(f"account_id:{account_id}")
        client.roles.get.assert_called_with(role_id)
        client.resources.list.assert_called_with(f'id:{resource_id}')
        assert grant_exists

    def test_when_grant_exists_not_using_access_rules(self, client, service):
        client.account_attachments.list = MagicMock(return_value=get_account_attachments())
        client.roles.get = MagicMock(return_value=get_role_response())
        client.resources.list = MagicMock(return_value=get_resource_list_iter())
        client.role_grants.list = MagicMock(return_value=[get_role_grant()])
        grant_exists = service.get_granted_resources_via_role([get_resource()], account_id)
        client.account_attachments.list.assert_called_with(f"account_id:{account_id}")
        client.roles.get.assert_called_with(role_id)
        client.role_grants.list.assert_called_with(f'role_id:{role_id}')
        assert grant_exists

    def test_when_grant_doesnt_exists(self, client, service):
        client.account_attachments.list = MagicMock(return_value=get_account_attachments())
        client.roles.get = MagicMock(return_value=get_role_response())
        client.roles.list = MagicMock(return_value=[get_role_response()])
        grant_exists = service.get_granted_resources_via_role([get_resource()], account_id)
        client.account_attachments.list.assert_called_with(f"account_id:{account_id}")
        client.roles.get.assert_called_with(role_id)
        client.resources.list.assert_not_called()
        assert not grant_exists

    def test_when_grant_exists_get_role_fail(self, client, service):
        error_message = "Role grant get failed"
        client.account_attachments.list = MagicMock(return_value=get_account_attachments())
        client.roles.get = MagicMock(side_effect=Exception(error_message))
        with pytest.raises(Exception) as ex:
            service.get_granted_resources_via_role([get_resource()], account_id)
        assert error_message in str(ex.value)

class Test_grant_temporary_access:
    def test_when_grant_is_possible(self, client, service):
        client.account_grants.create = MagicMock()
        service.grant_temporary_access(resource_id, account_id, grant_start_from, grant_valid_until)
        expected_sdm_grant = strongdm.AccountGrant(
            resource_id = resource_id,
            account_id = account_id,
            start_from = grant_start_from, 
            valid_until = grant_valid_until
        )
        actual_sdm_grant = client.account_grants.create.call_args[0][0]
        assert dir(expected_sdm_grant) == dir(actual_sdm_grant)

    def test_when_grant_is_not_possible(self, client, service):
        error_message = "Grant is not possible"
        client.account_grants.create = MagicMock(side_effect = Exception(error_message))
        with pytest.raises(Exception) as ex:
            service.grant_temporary_access(resource_id, account_id, grant_start_from, grant_valid_until)
        assert error_message in str(ex.value)

class Test_get_all_resources:
    def test_returns_resources(self, client, service):
        client.resources.list = MagicMock(return_value = get_resource_list_iter())
        sdm_resources = service.get_all_resources()
        assert len(sdm_resources) == 1
        assert sdm_resources[0].id == resource_id
        assert sdm_resources[0].name == resource_name

    def test_drop_none_resources(self, client, service): # useful for beta resources
        mock_resource = MagicMock()
        mock_resource.id = resource_id
        mock_resource.name = resource_name
        resource_list_iter = iter([mock_resource, None])

        client.resources.list = MagicMock(return_value = resource_list_iter)
        sdm_resources = service.get_all_resources()
        assert len(sdm_resources) == 1
        assert sdm_resources[0].id == resource_id
        assert sdm_resources[0].name == resource_name

    def test_with_filter(self, client, service):
        client.resources.list = MagicMock(side_effect = filter_resources)
        sdm_resources = service.get_all_resources(filter = "name:resource1")
        assert len(sdm_resources) == 1
        assert sdm_resources[0].id == resource_id
        assert sdm_resources[0].name == resource_name

    def test_no_resources_with_filter(self, client, service):
        client.resources.list = MagicMock(side_effect = filter_resources)
        sdm_resources = service.get_all_resources(filter = "name:resource2")
        assert len(sdm_resources) == 0


class Test_get_all_resources_by_role:
    def test_returns_resources_when_search_role_by_name(self, client, service):
        client.roles.list = MagicMock(return_value = get_role_iter(access_rules=[{'type':'postgres'}]))
        client.role_grants.list = MagicMock(return_value = get_role_grant_iter())
        client.resources.list = MagicMock(return_value = [get_resource()])
        resources = service.get_all_resources_by_role(role_name)
        client.roles.list.assert_called_with(f'name:?', role_name)
        client.role_grants.list.assert_called_with(f"role_id:{role_id}")
        assert client.resources.list.mock_calls == [call("id:1,id:2"), call("type:postgres")]
        assert len(resources) == 1

    def test_returns_resources_when_already_have_role(self, client, service):
        client.resources.list = MagicMock(return_value=[get_resource()])
        client.role_grants.list = MagicMock(return_value=[get_role_grant()])
        resources = service.get_all_resources_by_role(role_name, sdm_role=get_role())
        client.role_grants.list.assert_called_with(f"role_id:{role_id}")
        client.resources.list.assert_called_with(f"id:{resource_id}")
        assert len(resources) == 1

    def test_when_role_does_not_exist(self, client, service):
        client.roles.list = MagicMock(return_value = iter([]))
        with pytest.raises(Exception) as ex:
            service.get_all_resources_by_role(role_name)
        client.roles.list.assert_called_with('name:?', role_name)
        assert str(ex.value) != ""

    def test_when_role_grant_list_raises_exception(self, client, service):
        client.role_grants.list = MagicMock(side_effect=Exception())
        client.resources.list = MagicMock(return_value=[get_resource()])
        resources = service.get_all_resources_by_role(role_name, sdm_role=get_role(access_rules=[{'ids': [resource_id]}, {'type': 'postgres'}]))
        client.role_grants.list.assert_called_with(f"role_id:{role_id}")
        assert client.resources.list.mock_calls == [call(f"id:{resource_id}"), call("type:postgres")]
        assert len(resources) == 1

    def test_when_role_grant_list_returns_is_empty(self, client, service):
        client.role_grants.list = MagicMock(side_effect=iter([]))
        client.resources.list = MagicMock(return_value=[get_resource()])
        resources = service.get_all_resources_by_role(role_name, sdm_role=get_role(access_rules=[{'type': 'postgres'}]))
        client.role_grants.list.assert_called_with(f"role_id:{role_id}")
        assert client.resources.list.mock_calls == [call("type:postgres")]
        assert len(resources) == 1

    def test_when_have_role_grants_and_dont_have_access_rules(self, client, service):
        client.role_grants.list = MagicMock(return_value=[get_role_grant()])
        client.resources.list = MagicMock(return_value=[get_resource()])
        resources = service.get_all_resources_by_role(role_name, sdm_role=get_role())
        client.role_grants.list.assert_called_with(f"role_id:{role_id}")
        assert client.resources.list.mock_calls == [call(f"id:{resource_id}")]
        assert len(resources) == 1

    def test_with_filter(self, client, service):
        client.roles.list = MagicMock(return_value = get_role_iter())
        client.role_grants.list = MagicMock(return_value = get_role_grant_iter())
        client.resources.list = MagicMock(side_effect = filter_resources)
        sdm_resources = list(service.get_all_resources_by_role(role_name, filter=f"name:{resource_name}"))
        client.roles.list.assert_called_with(f'name:?', role_name)
        client.role_grants.list.assert_called_with(f"role_id:{role_id}")
        client.resources.list.assert_called_with(f"id:1,id:2,name:{resource_name}")
        assert len(sdm_resources) == 1
        assert sdm_resources[0].id == resource_id
        assert sdm_resources[0].name == resource_name

    def test_with_filter_and_access_rules(self, client, service):
        client.roles.list = MagicMock(return_value = get_role_iter(access_rules=[{"ids": [resource_id]}]))
        client.resources.list = MagicMock(side_effect = filter_resources)
        client.role_grants.list = MagicMock(return_value=[get_role_grant()])
        sdm_resources = list(service.get_all_resources_by_role(role_name, filter=f"name:{resource_name}"))

        client.roles.list.assert_called_with(f'name:?', role_name)
        client.resources.list.assert_called_with(f"id:{resource_id},name:{resource_name}")
        assert len(sdm_resources) == 1
        assert sdm_resources[0].id == resource_id
        assert sdm_resources[0].name == resource_name

    def test_no_resources_with_filter(self, client, service):
        nonexistent_resource = 'resource2'
        client.roles.list = MagicMock(return_value = get_role_iter())
        sdm_resources = service.get_all_resources_by_role(role_name, filter = f"name:{nonexistent_resource}")
        client.roles.list.assert_called_with(f'name:?', role_name)
        assert len(sdm_resources) == 0

    def test_no_resources_with_filter_and_access_rules(self, client, service):
        nonexistent_resource = 'resource2'
        client.roles.list = MagicMock(return_value = get_role_iter(access_rules=[{"ids": [resource_id]}]))
        client.role_grants.list = MagicMock(return_value=[get_role_grant()])
        client.resources.list = MagicMock(side_effect = filter_resources)
        sdm_resources = service.get_all_resources_by_role(role_name, filter = f"name:{nonexistent_resource}")
        client.roles.list.assert_called_with(f'name:?', role_name)
        client.role_grants.list.assert_called_with(f'role_id:{role_id}')
        client.resources.list.assert_called_with(f"id:{resource_id},name:{nonexistent_resource}")
        assert len(sdm_resources) == 0

class Test_get_role_by_name:
    def test_when_resource_exists_returns_role(self, client, service):
        client.roles.list = MagicMock(return_value = get_role_list_iter())
        sdm_role = service.get_role_by_name(resource_name)
        assert sdm_role.id == role_id
        assert sdm_role.name == role_name

    def test_when_sdm_client_fails_raises_exception(self, client, service):
        error_message = "SDM Client failed"
        client.roles.list = MagicMock(side_effect = Exception(error_message))
        with pytest.raises(Exception) as ex:
            service.get_role_by_name(resource_name)
        assert error_message in str(ex.value)

    def test_when_resource_doesnt_exist_raises_exception(self, client, service):
        client.roles.list = MagicMock(return_value = iter([]))
        with pytest.raises(Exception):
            service.get_role_by_name(resource_name)

class Test_get_all_roles:
    def test_returns_roles(self, client, service):
        client.roles.list = MagicMock(return_value = get_role_list_iter())
        sdm_roles = service.get_all_roles()
        assert len(sdm_roles) == 1
        assert sdm_roles[0].id == role_id
        assert sdm_roles[0].name == role_name


def get_resource_list_iter():
    mock_resource = get_resource()
    return iter([mock_resource])

def get_resource():
    mock_resource = MagicMock()
    mock_resource.id = resource_id
    mock_resource.name = resource_name
    mock_resource.role_id = role_id
    return mock_resource

def get_role_list_iter():
    return iter([get_role()])

def get_account_attachments():
    account_attachment = MagicMock()
    account_attachment.role_id = role_id
    account_attachment.account_id = account_id
    return iter([account_attachment])

def get_role_response(access_rules=None):
    response = MagicMock()
    response.role = get_role(access_rules)
    return response

def get_role(access_rules=None):
    mock_role = MagicMock()
    mock_role.id = role_id
    mock_role.name = role_name
    if access_rules:
        mock_role.access_rules = access_rules
    mock_role.to_dict = MagicMock(return_value=mock_role.__dict__)
    return mock_role

def get_role_iter(access_rules=None):
    mock_role = get_role(access_rules=access_rules)
    return iter([mock_role])

def get_role_grant():
    mock_role_grant = MagicMock()
    mock_role_grant.role_id = role_id
    mock_role_grant.resource_id = resource_id
    return mock_role_grant

def get_role_grant_iter():
    mock_role_grant1 = MagicMock()
    mock_role_grant1.resource_id = 1
    mock_role_grant2 = MagicMock()
    mock_role_grant2.resource_id = 2
    return iter([mock_role_grant1, mock_role_grant2])

def filter_resources(filter = ''):
    return [
        resource
        for resource in get_resource_list_iter()
        if not filter or resource.name in filter
    ]
