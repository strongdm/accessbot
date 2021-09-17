# pylint: disable=redefined-outer-name
# pylint: disable=invalid-name
import datetime
from datetime import timezone, timedelta
from unittest.mock import MagicMock
import pytest
import strongdm

from .sdm_service import SdmService

resource_id = 1
resource_name = "resource1"
role_id = 111
role_name = "role111"
account_id = 55
account_email = "myaccount@test.com"
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
        grant_exists = service.account_grant_exists(resource_id, account_id)
        client.account_grants.list.assert_called_with(f"resource_id:{resource_id},account_id:{account_id}")
        assert grant_exists is True

    def test_when_grant_doesnt_exists(self, client, service):
        client.account_grants.list = MagicMock(return_value=iter([]))
        grant_exists = service.account_grant_exists(resource_id, account_id)
        client.account_grants.list.assert_called_with(f"resource_id:{resource_id},account_id:{account_id}")
        assert grant_exists is False

    def test_when_grant_exists_fail(self, client, service):
        error_message = "Grant list failed"
        client.account_grants.list = MagicMock(side_effect = Exception(error_message))
        with pytest.raises(Exception) as ex:
            service.account_grant_exists(resource_id, account_id)
        assert error_message in str(ex.value)

# TODO Add tests for role_grant_exists

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

class Test_get_all_resources_by_role:
    def test_returns_resources(self, client, service):
        mock_role = MagicMock()
        mock_role.id = 111
        mock_role.name = "role_name"
        role_iter = iter([mock_role])
        client.roles.list = MagicMock(return_value = role_iter)

        mock_role_grant1 = MagicMock()
        mock_role_grant1.resource_id = 1
        mock_role_grant2 = MagicMock()
        mock_role_grant2.resource_id = 2
        role_grants_iter = iter([mock_role_grant1, mock_role_grant2])
        client.role_grants.list = MagicMock(return_value = role_grants_iter)

        client.resources.list = MagicMock(return_value = [None])

        resources = service.get_all_resources_by_role("role_name")
        client.roles.list.assert_called_with(('name:"role_name"'))
        client.role_grants.list.assert_called_with("role_id:111")
        client.resources.list.assert_called_with("id:1,id:2")
        assert len(resources) == 0 # discard None

    def test_when_role_does_not_exist(self, client, service):
        client.roles.list = MagicMock(return_value = iter([]))
        with pytest.raises(Exception) as ex:
            service.get_all_resources_by_role("role_name")
        client.roles.list.assert_called_with(('name:"role_name"'))
        assert str(ex.value) != ""

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
    mock_resource = MagicMock()
    mock_resource.id = resource_id
    mock_resource.name = resource_name
    return iter([mock_resource])

def get_role_list_iter():
    mock_role = MagicMock()
    mock_role.id = role_id
    mock_role.name = role_name
    return iter([mock_role])
