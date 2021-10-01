import shortuuid
from grant_request_type import GrantRequestType
from .base_grant_helper import BaseGrantHelper
from .exceptions import PermissionDeniedException
from .util import is_hidden_role

class RoleGrantHelper(BaseGrantHelper):
    def __init__(self, bot):
        self.__bot = bot
        self.__admin_ids = bot.get_admin_ids()
        self.__sdm_service = bot.get_sdm_service()

        super().__init__(bot, self.__sdm_service, self.__admin_ids, GrantRequestType.ASSIGN_ROLE, 'AUTO_APPROVE_ROLE_TAG', 'AUTO_APPROVE_ROLE_ALL')

    @staticmethod
    def generate_grant_request_id():
        return shortuuid.ShortUUID().random(length=4)

    def check_permission(self, sdm_object, sdm_account, searched_name):
        if not self.__allowed_to_assign_role(searched_name, sdm_account):
            raise PermissionDeniedException("Sorry, you\'re not allowed to get access to this role.\nContact an admin if you want to access to this role.")

    def get_all_items(self):
        return self.__sdm_service.get_all_roles()

    def get_item_by_name(self, name, execution_id = None):
        if is_hidden_role(self.__bot.config, name):
            self.__bot.log.info("##SDM## %s GrantHelper.get_item_by_name hidden role", name)
            raise Exception("Access to this role is not available via bot. Please see your strongDM admins.")
        return self.__sdm_service.get_role_by_name(name)

    def get_operation_desc(self):
        return "role assign"

    def can_try_fuzzy_matching(self):
        return True

    def __allowed_to_assign_role(self, role_name, sdm_account):
        if not self.__bot.config['USER_ROLES_TAG']:
            return True
        permitted_roles = sdm_account.tags.get(self.__bot.config['USER_ROLES_TAG']) if sdm_account.tags else ""
        return permitted_roles is None or role_name in permitted_roles
