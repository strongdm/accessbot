from .base_show_helper import BaseShowHelper
from ..util import is_hidden, HiddenTagEnum, is_concealed, AllowedTagEnum, is_allowed


class ShowResourcesHelper(BaseShowHelper):
    def __init__(self, bot):
        super().__init__(bot, "resources")

    def get_list(self, filter):
        role_name = self._bot.config["CONTROL_RESOURCES_ROLE_NAME"]
        if role_name is not None:
            resources = self._sdm_service.get_all_resources_by_role(role_name, filter = filter)
        else:
            resources = self._sdm_service.get_all_resources(filter = filter)
        return self.__filter_resources(resources)

    def get_line(self, item, sdm_account, message):
        if self.is_auto_approve(item):
            return f"* **{item.name} (type: {type(item).__name__}, auto-approve)**\n"
        return f"* {item.name} (type: {type(item).__name__})\n"

    def is_auto_approve(self, item):
        return (
            self._bot.config["AUTO_APPROVE_TAG"] is not None
            and self._bot.config["AUTO_APPROVE_TAG"] in item.tags
        )

    def __filter_resources(self, resources):
        return [
            resource
            for resource in resources
            if not is_hidden(self._bot.config, HiddenTagEnum.RESOURCE, resource)
            and not is_concealed(self._bot.config, resource)
            and is_allowed(self._bot.config, AllowedTagEnum.RESOURCE, resource)
        ]
