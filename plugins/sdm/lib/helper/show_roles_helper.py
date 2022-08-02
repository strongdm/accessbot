from .base_show_helper import BaseShowHelper
from ..util import is_hidden, HiddenTagEnum, AllowedTagEnum, is_allowed, AllowedGroupsTagEnum


class ShowRolesHelper(BaseShowHelper):
    def __init__(self, bot):
        super().__init__(bot, "roles")

    def get_list(self, filters, sdm_account):
        roles = self._sdm_service.get_all_roles()
        return self.__filter_roles(roles, sdm_account)

    def get_line(self, item, sdm_account):
        permitted_roles = sdm_account.tags.get(self._bot.config["USER_ROLES_TAG"])
        if self.__can_request_access(item, permitted_roles):
            if self.is_auto_approve(item):
                return r"* **" + item.name + r" (auto-approve)**" + "\n"
            return f"* {item.name}\n"
        return r"* " + self._bot.format_strikethrough(item.name) + " (not allowed)\n"

    def is_auto_approve(self, item):
        return self._bot.config["AUTO_APPROVE_ROLE_TAG"] in item.tags

    def __can_request_access(self, sdm_role, permitted_roles):
        return permitted_roles is None or sdm_role.name in permitted_roles

    def __filter_roles(self, roles, sdm_account):
        return [
            role
            for role in roles
            if not is_hidden(self._bot.config, HiddenTagEnum.ROLE, role)
            and is_allowed(self._bot.config, AllowedTagEnum.ROLE, AllowedGroupsTagEnum.ROLE, role, sdm_account)
        ]
