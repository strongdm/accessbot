import strongdm

def create_access_service(props, log):
    client = strongdm.Client(props.api_access_key(), props.api_secret_key())
    return AccessService(client, log)

class AccessService:
    def __init__(self, client, log):
        self.__client = client
        self.__log = log

    def get_resource_by_name(self, name):
        """
        Return a SDM resouce by name
        """
        try:
            self.__log.debug("************** AccessService.get_resource_by_name name: %s", name)
            sdm_resources = list(self.__client.resources.list('name:"{}"'.format(name)))
        except Exception as ex:
            raise Exception("List resources failed: " + str(ex)) from ex
        if len(sdm_resources) == 0:
            raise Exception("Sorry, cannot find that resource!")
        return sdm_resources[0]

    def get_account_by_email(self, email):
        """
        Return a SDM account by email
        """
        try:
            self.__log.debug("************** AccessService.get_account_by_email email: %s", email)
            sdm_accounts = list(self.__client.accounts.list('email:{}'.format(email)))
        except Exception as ex:
            raise Exception("List accounts failed: " + str(ex)) from ex
        if len(sdm_accounts) == 0:
            raise Exception("Sorry, cannot find your account!")
        return sdm_accounts[0]

    def grant_temporary_access(self, resource_id, account_id, start_from, valid_until):
        """
        Grant temporary access to a SDM resource for an account
        """
        try:
            self.__log.debug(
                "************** AccessService.grant_temporary_access resource_id: %s account_id: %d start_from: %s valid_until: %s",
                resource_id, account_id, start_from, valid_until
            )
            sdm_grant = strongdm.AccountGrant(
                resource_id = resource_id,
                account_id = account_id,
                start_from = start_from,
                valid_until = valid_until
            )
            self.__client.account_grants.create(sdm_grant)
        except Exception as ex:
            raise Exception("Grant failed: " + str(ex)) from ex

    def get_all_resources(self):
        """
        Return all resources
        """
        self.__log.debug("************** AccessService.get_all_resources")
        try:
            return list(self.__client.resources.list(''))
        except Exception as ex:
            raise Exception("List resources failed: " + str(ex)) from ex
