import datetime, re, time
from datetime import timezone, timedelta
import pytest
import strongdm
from unittest.mock import MagicMock

from access_service import AccessService
from properties import Properties

resource_id = 1
resource_name = "myresource"
account_id = 55
account_email = "myaccount@test.com"
grant_start_from = datetime.datetime.now(timezone.utc) + timedelta(minutes=1)
grant_valid_until = grant_start_from + timedelta(hours=1)


class Test_get_resource_by_name:
    @pytest.fixture(autouse=True)
    def before_each(self):
        self.client = MagicMock()
        self.service = AccessService(self.client)
        yield 

    def test_when_resource_exists_returns_resource(self):
        self.client.resources.list = MagicMock(return_value = self.get_resource_list_iter())
        sdm_resource = self.service.get_resource_by_name(resource_name)
        assert sdm_resource.id == resource_id
        assert sdm_resource.name == resource_name

    def test_when_sdm_client_fails_raises_exception(self):
        error_message = "SDM Client failed"
        self.client.resources.list = MagicMock(side_effect = Exception(error_message))
        with pytest.raises(Exception) as ex:
            self.service.get_resource_by_name(resource_name)
        assert error_message in str(ex.value)

    def test_when_resource_doesnt_exist_raises_exception(self):
        self.client.resources.list = MagicMock(return_value = iter([]))
        with pytest.raises(Exception):
            self.service.get_resource_by_name(resource_name)

    def get_resource_list_iter(self):
        mock_resource = MagicMock()
        mock_resource.id = resource_id
        mock_resource.name = resource_name
        return iter([mock_resource])


class Test_get_account_by_email:
    @pytest.fixture(autouse=True)
    def before_each(self):
        self.client = MagicMock()
        self.service = AccessService(self.client)
        yield 

    def test_when_account_exists_returns_account(self):
        self.client.accounts.list = MagicMock(return_value = self.get_account_list_iter())
        sdm_account = self.service.get_account_by_email(account_email)
        assert sdm_account.id == account_id
        assert sdm_account.email == account_email

    def test_when_sdm_client_fails_raises_exception(self):
        error_message = "SDM Client failed"
        self.client.accounts.list = MagicMock(side_effect = Exception(error_message))
        with pytest.raises(Exception) as ex:
            self.service.get_account_by_email(account_email)
        assert error_message in str(ex.value)

    def test_when_account_doesnt_exist_raises_exception(self):
        self.client.accounts.list = MagicMock(return_value = iter([]))
        with pytest.raises(Exception):
            self.service.get_account_by_email(account_email)

    def get_account_list_iter(self):
        mock_account = MagicMock()
        mock_account.id = account_id
        mock_account.email = account_email
        return iter([mock_account])


class Test_grant_temporary_access:
    @pytest.fixture(autouse=True)
    def before_each(self):
        self.client = MagicMock()
        self.service = AccessService(self.client)
        yield 

    def test_when_grant_is_possible(self):
        self.client.account_grants.create = MagicMock()
        sdm_account = self.service.grant_temporary_access(resource_id, account_id, grant_start_from, grant_valid_until)
        expected_sdm_grant = strongdm.AccountGrant(
            resource_id = resource_id,
            account_id = account_id,
            start_from = grant_start_from, 
            valid_until = grant_valid_until
        )
        actual_sdm_grant = self.client.account_grants.create.call_args[0][0]
        assert dir(expected_sdm_grant) == dir(actual_sdm_grant)

    def test_when_grant_is_not_possible(self):
        error_message = "Grant is not possible" # TODO Validate if it raises an exception
        self.client.account_grants.create = MagicMock(side_effect = Exception(error_message))
        with pytest.raises(Exception) as ex:
            self.service.grant_temporary_access(resource_id, account_id, grant_start_from, grant_valid_until)
        assert error_message in str(ex.value)
