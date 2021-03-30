import sdm_client
import strongdm

help_message = """
NAME: 
    accessbot - Manages access to strongDM resources via chatbots

COMMANDS:
    access to resource-name       - Grant access to a resource (using the requester's email address)
"""

class AccessService:
    def __init__(self, client):
        self.client = client

    def help(self):
        """
        Returns bot help
        """
        return help_message

    def get_resource_by_name(self, name):
        """
        Returns SDM resouce by name
        """
        try:
            sdm_resources = list(self.client.resources.list('name:"{}"'.format(name)))
        except Exception as ex:
            raise Exception("List resources failed: " + str(ex))
        if len(sdm_resources) == 0:
            raise Exception("Sorry, cannot find that resource!")
        return sdm_resources[0]

    def get_account_by_email(self, email):
        """
        Returns SDM account by email
        """
        try:
            sdm_accounts = list(self.client.accounts.list('email:{}'.format(email)))
        except Exception as ex:
            raise Exception("List accounts failed: " + str(ex))
        if len(sdm_accounts) == 0:
            raise Exception("Sorry, cannot find your account!")
        return sdm_accounts[0]

    def grant_temporary_access(self, resource_id, account_id, start_from, valid_until):
        """
        Grants temporary access to a SDM resource for an account
        """
        try:
            sdm_grant = strongdm.AccountGrant(
                resource_id = resource_id,
                account_id = account_id,
                start_from = start_from, 
                valid_until = valid_until
            )
            self.client.account_grants.create(sdm_grant)
        except Exception as ex:
            raise Exception("Grant failed: " + str(ex))


_INSTANCE = AccessService(sdm_client.create_client())
def create_service():
    return _INSTANCE

