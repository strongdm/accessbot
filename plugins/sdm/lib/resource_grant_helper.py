import shortuuid
from grant_request_type import GrantRequestType
from .base_grant_helper import BaseGrantHelper
from .exceptions import PermissionDeniedException
from .util import is_hidden_resource

class ResourceGrantHelper(BaseGrantHelper):
    def __init__(self, bot):
        self.__bot = bot
        self.__admin_ids = bot.get_admin_ids()
        self.__sdm_service = bot.get_sdm_service()
        super().__init__(bot, self.__sdm_service, self.__admin_ids, GrantRequestType.ACCESS_RESOURCE, 'AUTO_APPROVE_TAG', 'AUTO_APPROVE_ALL')

    @staticmethod
    def generate_grant_request_id():
        return shortuuid.ShortUUID().random(length=4)

    def check_permission(self, sdm_object, sdm_account, searched_name):
        if self.__sdm_service.grant_exists(sdm_object.id, sdm_account.id): # TODO Add tests for this branch
            raise PermissionDeniedException("You already have access to that resource!")

    def get_all_items(self):
        return self.__sdm_service.get_all_resources()

    def get_item_by_name(self, name, execution_id = None):
        return self.__get_resource(name, execution_id)

    def get_operation_desc(self):
        return "access"

    def can_try_fuzzy_matching(self):
        return not self.__bot.config['DISABLE_RESOURCES_FUZZY_MATCHING']

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
