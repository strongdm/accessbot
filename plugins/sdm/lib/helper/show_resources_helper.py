from .base_show_helper import BaseShowHelper
from ..util import is_hidden, HiddenTagEnum, is_concealed, AllowedTagEnum, is_allowed, can_auto_approve_by_tag, \
    AllowedGroupsTagEnum


class ShowResourcesHelper(BaseShowHelper):
    def __init__(self, bot):
        super().__init__(bot, "resources")

    def get_list(self, filter, sdm_account):
        role_name = self._bot.config["CONTROL_RESOURCES_ROLE_NAME"]
        if role_name is not None:
            resources = self._sdm_service.get_all_resources_by_role(role_name, filter = filter)
        else:
            resources = self._sdm_service.get_all_resources(filter = filter)
        return self.__filter_resources(resources, sdm_account)

    def get_line(self, item, _):
        if self.is_auto_approve(item):
            return f"* **{item.name} (type: {type(item).__name__}, auto-approve)**\n"
        details = [f'type: {type(item).__name__}']
        if self.has_auto_approve_groups(item):
            details.append(f'auto-approve-groups: "{item.tags[self._bot.config["AUTO_APPROVE_GROUPS_TAG"]]}"')
        return f"* {item.name} ({', '.join(details)})\n"

    def is_auto_approve(self, item):
        return can_auto_approve_by_tag(self._bot.config, item, "AUTO_APPROVE_TAG")

    def has_auto_approve_groups(self, item):
        return (
            self._bot.config["AUTO_APPROVE_GROUPS_TAG"] is not None
            and self._bot.config["GROUPS_TAG"] is not None
            and self._bot.config["AUTO_APPROVE_GROUPS_TAG"] in item.tags
            and item.tags[self._bot.config["AUTO_APPROVE_GROUPS_TAG"]] is not None
        )

    def __filter_resources(self, resources, sdm_account):
        return [
            resource
            for resource in resources
            if not is_hidden(self._bot.config, HiddenTagEnum.RESOURCE, resource)
            and not is_concealed(self._bot.config, resource)
            and is_allowed(self._bot.config, AllowedTagEnum.RESOURCE, AllowedGroupsTagEnum.RESOURCE, resource, sdm_account)
        ]
