import json

from ..exceptions import NotFoundException
import strongdm

def create_sdm_service(api_access_key, api_secret_key, log):
    client = strongdm.Client(api_access_key, api_secret_key)
    return SdmService(client, log)

class SdmService:
    def __init__(self, client, log):
        self.__client = client
        self.__log = log

    def get_resource_by_name(self, name):
        """
        Return a SDM resouce by name
        """
        try:
            self.__log.debug("##SDM## SdmService.get_resource_by_name name: %s", name)
            sdm_resources = list(self.__client.resources.list('name:?', name))
        except Exception as ex:
            raise Exception("List resources failed: " + str(ex)) from ex
        if len(sdm_resources) == 0:
            raise NotFoundException("Sorry, cannot find that resource!")
        return sdm_resources[0]

    def get_account_by_email(self, email):
        """
        Return a SDM account by email
        """
        try:
            self.__log.debug("##SDM## SdmService.get_account_by_email email: %s", email)
            sdm_accounts = list(self.__client.accounts.list('email:{}'.format(email)))
        except Exception as ex:
            raise Exception("List accounts failed: " + str(ex)) from ex
        if len(sdm_accounts) == 0:
            raise Exception("Sorry, cannot find your account!")
        return sdm_accounts[0]

    def get_account_by_name(self, name):
        """
        Retrieves an account by name
        """
        try:
            self.__log.debug("##SDM## SdmService.get_account_by_name name: %s", name)
            sdm_accounts = list(self.__client.accounts.list('name:"{}"'.format(name)))
        except Exception as ex:
            raise Exception("List accounts failed: " + str(ex)) from ex
        if len(sdm_accounts) == 0:
            raise Exception("Sorry, cannot find your account!")
        return sdm_accounts[0]

    def reinstate_account(self, account):
        """
        Reinstate an account
        """
        try:
            self.__log.debug("##SDM## SdmService.reinstate_account account_id: %s", account.id)
            account.suspended = False
            return self.__client.accounts.update(account)
        except Exception as ex:
            raise Exception("Reinstate account failed: " + str(ex)) from ex

    def suspend_account(self, account):
        """
        Suspend an account
        """
        try:
            self.__log.debug("##SDM## SdmService.suspend_account account_id: %s", account.id)
            account.suspended = True
            return self.__client.accounts.update(account)
        except Exception as ex:
            raise Exception("Reinstate account failed: " + str(ex)) from ex

    def account_grant_exists(self, resource, account_id):
        """
        Does an account grant exists - resource assigned to an account
        """
        self.__log.debug("##SDM## SdmService.account_grant_exists resource_id: %s account_id: %s", resource.id, account_id)
        return len(self.get_granted_resources_via_account([resource], account_id)) > 0

    def get_granted_resources_via_account(self, resources, account_id):
        """
        A list of resources assigned to an account
        """
        granted_resources = []
        try:
            for resource in resources:
                self.__log.debug("##SDM## SdmService.account_grant_exists resource_id: %s account_id: %s", resource.id, account_id)
                account_grants = list(self.__client.account_grants.list(f"resource_id:{resource.id},account_id:{account_id}"))
                if len(account_grants) > 0:
                    granted_resources.append(resource)
        except Exception as ex:
            raise Exception("Account grant exists failed: " + str(ex)) from ex
        return granted_resources

    def delete_account_grant(self, resource_id, account_id):
        """
        Deletes an account grant from a resource assigned to an account
        """
        try:
            self.__log.debug("##SDM## SdmService.delete_account_grant resource_id: %s account_id: %s", resource_id, account_id)
            account_grants = list(self.__client.account_grants.list(f"resource_id:{resource_id},account_id:{account_id}"))
            if len(account_grants) > 0:
                self.__client.account_grants.delete(account_grants[0].id)
        except Exception as ex:
            raise Exception("Delete account grant failed: " + str(ex)) from ex

    def get_granted_resources_via_role(self, sdm_resources, account_id):
        """
        A list of resources assigned to an account via a role

        account -> account_attachment -> role -> (role_grant|access_rules) -> resource
        """
        granted_resources = []
        try:
            for aa in list(self.__client.account_attachments.list(f"account_id:{account_id}")):
                role = self.__client.roles.get(aa.role_id).role
                for role_resource in self.get_all_resources_by_role(role.name, sdm_role=role):
                    granted_resources += [sdm_resource for sdm_resource in sdm_resources if role_resource.id == sdm_resource.id]
        except Exception as ex:
            raise Exception("Role grant exists failed: " + str(ex)) from ex
        return granted_resources

    def grant_temporary_access(self, resource_id, account_id, start_from, valid_until):
        """
        Grant temporary access to a SDM resource for an account
        """
        try:
            self.__log.debug(
                "##SDM## SdmService.grant_temporary_access resource_id: %s account_id: %s start_from: %s valid_until: %s",
                resource_id, account_id, str(start_from), str(valid_until)
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

    def get_all_resources(self, filter = ''):
        """
        Return all resources
        """
        self.__log.debug("##SDM## SdmService.get_all_resources")
        try:
            return self.remove_none_values(self.__client.resources.list(filter))
        except Exception as ex:
            raise Exception("List resources failed: " + str(ex)) from ex

    def get_role_by_name(self, name):
        """
        Return a SDM role by name
        """
        self.__log.debug("##SDM## SdmService.get_role_by_name name: %s", name)
        try:
            sdm_roles = list(self.__client.roles.list('name:?', name))
        except Exception as ex:
            raise Exception("List roles failed: " + str(ex)) from ex
        if len(sdm_roles) == 0:
            raise Exception("Sorry, cannot find that role!")
        return sdm_roles[0]

    def get_all_roles(self):
        """
        Return all roles
        """
        try:
            self.__log.debug("##SDM## SdmService.get_all_roles")
            return list(self.__client.roles.list(''))
        except Exception as ex:
            raise Exception("List roles failed: " + str(ex)) from ex

    # TODO Create 2 methods: get_all_resources_by_role_name and get_all_resources_by_role
    def get_all_resources_by_role(self, role_name, filter='', sdm_role=None):
        """
        Return all resources by role name
        """
        self.__log.debug(
            "##SDM## SdmService.get_all_resources_by_role role_name: %s filter: %s sdm_role: %s",
            role_name,
            filter,
            str(sdm_role)
        )
        try:
            if not sdm_role:
                sdm_role = self.get_role_by_name(role_name)
            resources_filters = self.__get_resources_filters_by_role(sdm_role)
            if filter:
                resources_filters = [f"{rf},{filter}" for rf in resources_filters]
            return self.__get_unique_resources(resources_filters)
        except Exception as ex:
            raise Exception("List resources by role failed: " + str(ex)) from ex

    def __get_resources_filters_by_role(self, sdm_role):
        resources_filters = []
        role_grants_executed = True
        try:
            sdm_role_grants = list(self.__client.role_grants.list(f"role_id:{sdm_role.id}"))
            if len(sdm_role_grants) > 0:
                rules = ",".join([f"id:{rg.resource_id}" for rg in sdm_role_grants])
                resources_filters.append(rules)
        except Exception as ex:
            self.__log.debug("##SDM## SdmService.__get_resources_filters_by_role RoleGrants.list failed, interpreting access_rules attribute (Access Overhaul enabled?) " + str(ex))
            role_grants_executed = False
        access_rules = json.loads(sdm_role.access_rules) if isinstance(sdm_role.access_rules, str) else sdm_role.access_rules
        for ar in access_rules:
            filters = []
            if not role_grants_executed and ar.get('ids'):
                filters.append(",".join([f"id:{id}" for id in ar['ids']]))
            if ar.get('type'):
                filters.append(f"type:{ar['type']}")
            if ar.get('tags'):
                tags = []
                for key, value in ar['tags'].items():
                    tags.append('tag:"{}"="{}"'.format(key, value))
                filters.append(",".join(tags))
            if len(filters) > 0:
                resources_filters.append(",".join(filters))
        return resources_filters

    def __get_unique_resources(self, resources_filter):
        resources_map = {}
        for filter in resources_filter:
            resources = self.remove_none_values(self.__client.resources.list(filter))
            resources_map |= {r.id: r for r in resources if resources_map.get(r.id) is None}
        return resources_map.values()

    @staticmethod
    def remove_none_values(elements):
        return [e for e in elements if e is not None]

    def attach_role_to_account(self, role_id, account_id):
        try:
            grant = strongdm.AccountAttachment(
                role_id=role_id,
                account_id=account_id
            )
            return self.__client.account_attachments.create(grant)
        except strongdm.errors.AlreadyExistsError:
            self.__log.info("##SDM## SdmService.attach_role_to_account AccountAttachments.Create failed due to an already existing attachment. The sa attachment expiry entry will be renewed")
            return None
        except Exception as ex:
            raise Exception(f"An error occurred when attaching role to the provided account: {str(ex)}") from ex
