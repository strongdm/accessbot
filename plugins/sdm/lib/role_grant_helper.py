import shortuuid
from grant_request_type import GrantRequestType
from .exceptions import NotFoundException
from .base_grant_helper import BaseGrantHelper

class RoleGrantHelper(BaseGrantHelper):
    def __init__(self, bot):
        self.__bot = bot
        self.__admin_ids = bot.get_admin_ids()
        self.__sdm_service = bot.get_sdm_service()

        super().__init__(bot, self.__sdm_service, self.__admin_ids, 'role', GrantRequestType.ASSIGN_ROLE, 'AUTO_APPROVE_ROLE_TAG', 'AUTO_APPROVE_ROLE_ALL')

    def assign_role(self, message, role_name):
        execution_id = shortuuid.ShortUUID().random(length=6)
        self.__bot.log.info("##SDM## %s GrantHelper.assign_role new access request for role_name: %s", execution_id, role_name)
        try:
            sdm_role = self.__get_role(role_name)
            sdm_account = super().get_account(message)
            if not self.__allowed_to_assign_role(role_name, sdm_account):
                yield "Sorry, you\'re not allowed to get access to this role.\nContact an admin if you want to access to this role."
                return
            request_id = self.generate_grant_request_id()
            yield from super().grant_access(message, sdm_role, sdm_account, execution_id, request_id)
        except NotFoundException as ex:
            self.__bot.log.error("##SDM## %s GrantHelper.assign_role access request failed %s", execution_id, str(ex))
            yield str(ex)
            roles = self.__sdm_service.get_all_roles()
            yield from super().try_fuzzy_matching(execution_id, roles, role_name)

    @staticmethod
    def generate_grant_request_id():
        return BaseGrantHelper.generate_grant_request_id()

    def __get_role(self, role_name):
        return self.__sdm_service.get_role_by_name(role_name)

    def __allowed_to_assign_role(self, role_name, sdm_account):
        if not self.__bot.config['USER_ROLES_TAG']:
            return True
        permitted_roles = sdm_account.tags.get(self.__bot.config['USER_ROLES_TAG']) if sdm_account.tags else None
        return permitted_roles and len(permitted_roles) > 0 and role_name in permitted_roles.split(',')
