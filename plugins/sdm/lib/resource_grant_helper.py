import shortuuid
from grant_request_type import GrantRequestType
from .base_grant_helper import BaseGrantHelper
from .exceptions import NotFoundException
from .util import is_hidden_resource


class ResourceGrantHelper(BaseGrantHelper):
    def __init__(self, bot):
        self.__bot = bot
        self.__admin_ids = bot.get_admin_ids()
        self.__sdm_service = bot.get_sdm_service()

        super().__init__(bot, self.__sdm_service, self.__admin_ids, 'resource', GrantRequestType.ACCESS_RESOURCE, 'AUTO_APPROVE_TAG', 'AUTO_APPROVE_ALL')

    def access_resource(self, message, resource_name):
        execution_id = shortuuid.ShortUUID().random(length=6)
        self.__bot.log.info("##SDM## %s GrantHelper.access_resource new access request for resource_name: %s", execution_id, resource_name)
        try:
            sdm_resource = self.__get_resource(resource_name, execution_id)
            sdm_account = super().get_account(message)
            if self.__sdm_service.grant_exists(sdm_resource.id, sdm_account.id): # TODO Add tests for this branch
                yield "You already have access to that resource!"
                return
            request_id = self.generate_grant_request_id()
            yield from super().grant_access(message, sdm_resource, sdm_account, execution_id, request_id)
        except NotFoundException as ex:
            self.__bot.log.error("##SDM## %s GrantHelper.access_resource access request failed %s", execution_id, str(ex))
            yield str(ex)
            resources = self.__sdm_service.get_all_resources()
            yield from super().try_fuzzy_matching(execution_id, resources, resource_name)

    @staticmethod
    def generate_grant_request_id():
        return super.generate_grant_request_id()

    def __get_resource(self, resource_name, execution_id):
        role_name = self.__bot.config['CONTROL_RESOURCES_ROLE_NAME']
        if role_name and not self.__is_resource_in_role(resource_name, role_name):
            self.__bot.log.info("##SDM## %s GrantHelper.__get_resource resource not in role %s", execution_id, role_name)
            raise Exception("Access to this resource not available via bot. Please see your strongDM admins.")
        sdm_resource = self.__sdm_service.get_resource_by_name(resource_name)
        if is_hidden_resource(self.__bot.config, sdm_resource):
            self.__bot.log.info("##SDM## %s GrantHelper.__get_resource hidden resource", execution_id)
            raise Exception("Access to this resource not available via bot. Please see your strongDM admins.")
        return sdm_resource

    def __is_resource_in_role(self, resource_name, role_name):
        sdm_resources_by_role = self.__sdm_service.get_all_resources_by_role(role_name)
        return any(r.name == resource_name for r in sdm_resources_by_role)
