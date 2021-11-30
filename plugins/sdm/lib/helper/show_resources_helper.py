from .base_show_helper import BaseShowHelper
from ..util import is_hidden, HiddenTagEnum, AllowedTagEnum, is_allowed


class ShowResourcesHelper(BaseShowHelper):
    def __init__(self, bot):
        self.__bot = bot
        self.__sdm_service = bot.get_sdm_service()
        super().__init__("resources")

    def get_list(self, filters = None):
        role_name = self.__bot.config["CONTROL_RESOURCES_ROLE_NAME"]
        if role_name is not None:
            resources = self.__sdm_service.get_all_resources_by_role(role_name, filters = filters)
        else:
            resources = self.__sdm_service.get_all_resources(filters = filters)
        return self.__filter_resources(resources)

    def get_line(self, item, message = ''):
        if self.is_auto_approve(item):
            return f"* **{item.name} (type: {type(item).__name__}, auto-approve)**\n"
        return f"* {item.name} (type: {type(item).__name__})\n"

    def is_auto_approve(self, item):
        return (
            self.__bot.config["AUTO_APPROVE_TAG"] is not None
            and self.__bot.config["AUTO_APPROVE_TAG"] in item.tags
        )

    def __filter_resources(self, resources):
        return [
            resource
            for resource in resources
            if not is_hidden(self.__bot.config, HiddenTagEnum.RESOURCE, resource)
            and is_allowed(self.__bot.config, AllowedTagEnum.RESOURCE, resource)
        ]
